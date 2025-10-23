"""
Network Intelligence Module
Performs network reconnaissance and port scanning
"""

import socket
import asyncio
from typing import Dict, Any, List
from datetime import datetime


class NetworkIntelligence:
    """Network reconnaissance module"""
    
    def __init__(self):
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995,
            3306, 3389, 5432, 5900, 8080, 8443, 27017
        ]
        self.timeout = 2
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Perform network intelligence gathering
        
        Args:
            target: Domain or IP address to scan
            
        Returns:
            Dictionary containing network intelligence
        """
        results = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "open_ports": [],
            "closed_ports": [],
            "services": {},
            "banners": {}
        }
        
        # Resolve domain to IP if needed
        try:
            ip_address = socket.gethostbyname(target)
            results["ip_address"] = ip_address
        except Exception as e:
            results["error"] = f"Could not resolve hostname: {str(e)}"
            return results
        
        # Scan common ports
        tasks = [self._scan_port(ip_address, port) for port in self.common_ports]
        port_results = await asyncio.gather(*tasks)
        
        for port, is_open, banner in port_results:
            if is_open:
                results["open_ports"].append(port)
                service = self._identify_service(port)
                results["services"][port] = service
                if banner:
                    results["banners"][port] = banner
            else:
                results["closed_ports"].append(port)
        
        return results
    
    async def _scan_port(self, host: str, port: int) -> tuple:
        """
        Scan a single port
        
        Args:
            host: IP address or hostname
            port: Port number to scan
            
        Returns:
            Tuple of (port, is_open, banner)
        """
        try:
            # Create connection with timeout
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.timeout
            )
            
            # Try to grab banner
            banner = None
            try:
                banner_data = await asyncio.wait_for(
                    reader.read(1024),
                    timeout=1
                )
                banner = banner_data.decode('utf-8', errors='ignore').strip()
            except:
                pass
            
            writer.close()
            await writer.wait_closed()
            
            return (port, True, banner)
            
        except:
            return (port, False, None)
    
    def _identify_service(self, port: int) -> str:
        """Identify common services by port number"""
        services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            465: "SMTPS",
            587: "SMTP (Submission)",
            993: "IMAPS",
            995: "POP3S",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt",
            27017: "MongoDB"
        }
        return services.get(port, "Unknown")

