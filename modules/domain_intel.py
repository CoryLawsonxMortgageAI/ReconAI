"""
Domain Intelligence Module
Gathers DNS, WHOIS, and subdomain information
"""

import dns.resolver
import whois
import socket
from typing import Dict, Any, List
from datetime import datetime


class DomainIntelligence:
    """Domain reconnaissance module"""
    
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Perform domain intelligence gathering
        
        Args:
            target: Domain name to scan
            
        Returns:
            Dictionary containing domain intelligence
        """
        results = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "whois": {},
            "dns_records": {},
            "subdomains": [],
            "ip_addresses": [],
            "nameservers": [],
            "mail_servers": []
        }
        
        # WHOIS lookup
        try:
            whois_data = whois.whois(target)
            results["whois"] = {
                "registrar": getattr(whois_data, 'registrar', 'N/A'),
                "creation_date": str(getattr(whois_data, 'creation_date', 'N/A')),
                "expiration_date": str(getattr(whois_data, 'expiration_date', 'N/A')),
                "name_servers": getattr(whois_data, 'name_servers', []),
                "status": getattr(whois_data, 'status', 'N/A'),
                "emails": getattr(whois_data, 'emails', []),
                "org": getattr(whois_data, 'org', 'N/A'),
                "country": getattr(whois_data, 'country', 'N/A')
            }
        except Exception as e:
            results["whois"]["error"] = str(e)
        
        # DNS Records
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = self.resolver.resolve(target, record_type)
                results["dns_records"][record_type] = [str(rdata) for rdata in answers]
                
                # Extract specific information
                if record_type == 'A':
                    results["ip_addresses"].extend([str(rdata) for rdata in answers])
                elif record_type == 'NS':
                    results["nameservers"].extend([str(rdata) for rdata in answers])
                elif record_type == 'MX':
                    results["mail_servers"].extend([str(rdata) for rdata in answers])
                    
            except Exception as e:
                results["dns_records"][record_type] = []
        
        # Subdomain enumeration (common subdomains)
        common_subdomains = [
            'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'admin', 'api', 'dev', 'staging', 'test', 'blog', 'shop',
            'vpn', 'remote', 'portal', 'support', 'help', 'docs'
        ]
        
        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{target}"
            try:
                answers = self.resolver.resolve(full_domain, 'A')
                results["subdomains"].append({
                    "subdomain": full_domain,
                    "ip_addresses": [str(rdata) for rdata in answers]
                })
            except:
                pass
        
        # Reverse DNS lookup
        results["reverse_dns"] = []
        for ip in results["ip_addresses"][:5]:  # Limit to first 5 IPs
            try:
                hostname = socket.gethostbyaddr(ip)
                results["reverse_dns"].append({
                    "ip": ip,
                    "hostname": hostname[0]
                })
            except:
                pass
        
        return results

