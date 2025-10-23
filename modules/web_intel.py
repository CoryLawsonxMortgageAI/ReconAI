"""
Web Intelligence Module
Analyzes web applications and HTTP services
"""

import aiohttp
import ssl
import socket
from typing import Dict, Any
from datetime import datetime
from urllib.parse import urlparse


class WebIntelligence:
    """Web application reconnaissance module"""
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=10)
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Perform web intelligence gathering
        
        Args:
            target: Domain or URL to scan
            
        Returns:
            Dictionary containing web intelligence
        """
        results = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "http_headers": {},
            "https_headers": {},
            "security_headers": {},
            "technologies": [],
            "ssl_info": {},
            "robots_txt": None,
            "sitemap": None,
            "status_codes": {}
        }
        
        # Ensure target has protocol
        if not target.startswith(('http://', 'https://')):
            http_url = f"http://{target}"
            https_url = f"https://{target}"
        else:
            parsed = urlparse(target)
            http_url = f"http://{parsed.netloc}"
            https_url = f"https://{parsed.netloc}"
        
        # HTTP Headers Analysis
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            # Try HTTPS first
            try:
                async with session.get(https_url, ssl=False) as response:
                    results["status_codes"]["https"] = response.status
                    results["https_headers"] = dict(response.headers)
                    
                    # Analyze security headers
                    results["security_headers"] = self._analyze_security_headers(response.headers)
                    
                    # Detect technologies
                    results["technologies"] = self._detect_technologies(response.headers)
                    
            except Exception as e:
                results["https_headers"]["error"] = str(e)
            
            # Try HTTP
            try:
                async with session.get(http_url, ssl=False) as response:
                    results["status_codes"]["http"] = response.status
                    results["http_headers"] = dict(response.headers)
            except Exception as e:
                results["http_headers"]["error"] = str(e)
            
            # Check robots.txt
            try:
                async with session.get(f"{https_url}/robots.txt", ssl=False) as response:
                    if response.status == 200:
                        results["robots_txt"] = await response.text()
            except:
                pass
            
            # Check sitemap
            try:
                async with session.get(f"{https_url}/sitemap.xml", ssl=False) as response:
                    if response.status == 200:
                        results["sitemap"] = "Found"
            except:
                pass
        
        # SSL/TLS Certificate Analysis
        try:
            results["ssl_info"] = self._get_ssl_info(target)
        except Exception as e:
            results["ssl_info"]["error"] = str(e)
        
        return results
    
    def _analyze_security_headers(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """Analyze HTTP security headers"""
        security_headers = {
            "Strict-Transport-Security": headers.get("Strict-Transport-Security", "Missing"),
            "Content-Security-Policy": headers.get("Content-Security-Policy", "Missing"),
            "X-Frame-Options": headers.get("X-Frame-Options", "Missing"),
            "X-Content-Type-Options": headers.get("X-Content-Type-Options", "Missing"),
            "X-XSS-Protection": headers.get("X-XSS-Protection", "Missing"),
            "Referrer-Policy": headers.get("Referrer-Policy", "Missing"),
            "Permissions-Policy": headers.get("Permissions-Policy", "Missing")
        }
        
        # Calculate security score
        present = sum(1 for v in security_headers.values() if v != "Missing")
        security_headers["score"] = f"{present}/7"
        security_headers["grade"] = self._calculate_grade(present, 7)
        
        return security_headers
    
    def _calculate_grade(self, score: int, total: int) -> str:
        """Calculate letter grade from score"""
        percentage = (score / total) * 100
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    def _detect_technologies(self, headers: Dict[str, str]) -> list:
        """Detect web technologies from headers"""
        technologies = []
        
        server = headers.get("Server", "").lower()
        if "nginx" in server:
            technologies.append("Nginx")
        elif "apache" in server:
            technologies.append("Apache")
        elif "cloudflare" in server:
            technologies.append("Cloudflare")
        elif "microsoft" in server or "iis" in server:
            technologies.append("IIS")
        
        powered_by = headers.get("X-Powered-By", "").lower()
        if "php" in powered_by:
            technologies.append("PHP")
        elif "asp.net" in powered_by:
            technologies.append("ASP.NET")
        
        return technologies
    
    def _get_ssl_info(self, target: str) -> Dict[str, Any]:
        """Get SSL/TLS certificate information"""
        ssl_info = {}
        
        try:
            # Remove protocol if present
            if target.startswith(('http://', 'https://')):
                target = urlparse(target).netloc
            
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_info["subject"] = dict(x[0] for x in cert.get("subject", []))
                    ssl_info["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                    ssl_info["version"] = cert.get("version")
                    ssl_info["serial_number"] = cert.get("serialNumber")
                    ssl_info["not_before"] = cert.get("notBefore")
                    ssl_info["not_after"] = cert.get("notAfter")
                    ssl_info["protocol"] = ssock.version()
                    
                    # Subject Alternative Names
                    san = cert.get("subjectAltName", [])
                    ssl_info["san"] = [name[1] for name in san]
                    
        except Exception as e:
            ssl_info["error"] = str(e)
        
        return ssl_info

