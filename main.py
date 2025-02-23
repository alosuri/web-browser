import socket
import ssl

class URL:
    def __init__(self, url: str) -> None:
        self.scheme, url = url.split("://", 1)
        # Make sure website is on http server, otherwise show error
        assert self.scheme in ["http", "https"]

        match self.scheme:
            case "http":
                self.port = 80
            case "https":
                self.port = 443

        if "/" not in url:
            url += "/"
        
        # Host is our main website, like facebook.com, web.whatsapp.com etc.
        self.host, url = url.split("/", 1)
        # Path on the other site is specific place on that page for example alosuri.github.io/portoflio <- /portfolio is path
        self.path: str = "/" + url

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self) -> str:
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))

        if (self.scheme == "https"):
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        # Send data to other server
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8"))

        # Recived info from server
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content
    
def show(body) -> None:
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url) -> None:
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))