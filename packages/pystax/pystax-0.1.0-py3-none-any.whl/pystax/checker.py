import socket
import http.client
import ssl


class DomainProbe:
    def __init__(self):
        self.conn = None

    def probe_domain(self, domain):
        try:
            if domain.lower() == "localhost" or domain == "127.0.0.1":
                return "HTTP", 200

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.load_default_certs()

            self.conn = http.client.HTTPSConnection(domain, timeout=5, context=context)
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            return "HTTPS", response.status
        except (socket.gaierror, http.client.HTTPException):
            try:
                self.conn = http.client.HTTPConnection(domain, timeout=5)
                self.conn.request("GET", "/")
                response = self.conn.getresponse()
                return "HTTP", response.status
            except (socket.gaierror, http.client.HTTPException):
                return "Error: Unable to connect to the domain"
            except socket.timeout:
                return "Error: Connection timed out"
            except http.client.InvalidURL:
                return "Error: Invalid domain"
        except socket.timeout:
            return "Error: Connection timed out"
        except ssl.SSLCertVerificationError:
            return "Error: SSL certificate verification failed"
        finally:
            if self.conn:
                self.conn.close()

    def probe_ip(self, ip_address):
        try:
            if ip_address == "127.0.0.1":
                return "HTTP", 200

            self.conn = http.client.HTTPConnection(ip_address, timeout=5)
            self.conn.request("GET", "/")
            response = self.conn.getresponse()
            return "HTTP", response.status
        except (socket.gaierror, http.client.HTTPException):
            return "Error: Unable to connect to the IP address"
        except socket.timeout:
            return "Error: Connection timed out"
        except http.client.InvalidURL:
            return "Error: Invalid IP address"
        finally:
            if self.conn:
                self.conn.close()

