import logging
import re
import socket
import threading

# demo_logging_1.load_loggingconfig()
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s>%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class ClientClass(object):
    """docstring for ClientClass"""
    __HOST = "192.168.58.1"
    __PORT = 9898

    def __init__(self):
        self.__TCP_SOCKET = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        # 服务端的地址 address
        self.__ADDR = (ClientClass.__HOST, ClientClass.__PORT)
        self.__username = None

    @property
    def get_username(self):
        return self.__username

    @get_username.setter
    def set_username(self, username):
        self.__username = username

    def start_client(self):
        """启动客户端"""
        with self.__TCP_SOCKET as sock:
            # 链接服务端地址
            sock.connect(self.__ADDR)
            # 接收来自服务端的登录信息
            recv_data = sock.recv(1024).decode("utf-8")
            logger.info(recv_data)
            # 设置昵称 进入
            self.set_username = self.register_username(sock)
            recv_t = threading.Thread(
                target=self.recv_data, args=(sock,))
            # 向服务端发送数据
            send_t = threading.Thread(
                target=self.send_data, args=(sock,))
            # 接收数据线程设置为守护线程
            recv_t.setDaemon(True)
            recv_t.start()
            send_t.start()
            send_t.join()

    def send_data(self, sock):
        while True:
            send_data = input(f"{self.get_username}:")
            sock.sendall(str(send_data).encode("utf-8"))
            # 如果输入 quit 或者 exit 断开连接
            if send_data in ("quit", "exit"):
                logger.info("正在退出...")
                break

    def recv_data(self, sock):
        while True:
            try:
                recv_data = sock.recv(1024).decode("utf-8")
                logger.info(recv_data)

            except Exception as e:
                logger.error(e, exc_info=True)

    def register_username(self, sock):
        """注册客户端昵称"""
        username = input()
        sock.sendall(username.encode("utf-8"))
        recv_data = sock.recv(1024).decode("utf-8")
        logger.info(recv_data)
        if re.match(r"OK.*", recv_data):
            return username
        self.register_username(sock)


if __name__ == '__main__':
    ClientClass().start_client()
    # 创建一个新线程，用于接收服务器端的消息

