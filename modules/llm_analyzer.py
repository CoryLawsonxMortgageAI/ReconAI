"""
LLM Analyzer Module
Uses GPT-4 to analyze and correlate OSINT findings
"""

import os
import json
from typing import Dict, Any
from datetime import datetime
from openai import OpenAI


class LLMAnalyzer:
    """LLM-powered intelligence analysis and correlation"""
    
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4.1-mini"
    
    async def analyze(self, target: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze reconnaissance results using LLM
        
        Args:
            target: Target domain/IP
            results: Dictionary of module results
            
        Returns:
            Analysis and recommendations
        """
        analysis = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "summary": "",
            "risk_score": 0,
            "attack_surface": {},
            "vulnerabilities": [],
            "recommendations": [],
            "correlations": []
        }
        
        # Prepare data for LLM
        intelligence_data = self._prepare_intelligence_data(results)
        
        # Generate comprehensive analysis
        try:
            analysis["summary"] = await self._generate_summary(target, intelligence_data)
            analysis["risk_score"] = await self._calculate_risk_score(intelligence_data)
            analysis["attack_surface"] = await self._analyze_attack_surface(intelligence_data)
            analysis["vulnerabilities"] = await self._identify_vulnerabilities(intelligence_data)
            analysis["recommendations"] = await self._generate_recommendations(target, intelligence_data)
            analysis["correlations"] = await self._find_correlations(intelligence_data)
        except Exception as e:
            analysis["error"] = f"LLM analysis failed: {str(e)}"
        
        return analysis
    
    def _prepare_intelligence_data(self, results: Dict[str, Any]) -> str:
        """Prepare intelligence data for LLM analysis"""
        # Create a structured summary of findings
        summary_parts = []
        
        # Domain intelligence
        if "domain" in results:
            domain_data = results["domain"]
            summary_parts.append(f"Domain Intelligence:")
            summary_parts.append(f"- IP Addresses: {', '.join(domain_data.get('ip_addresses', []))}")
            summary_parts.append(f"- Nameservers: {', '.join(domain_data.get('nameservers', []))}")
            summary_parts.append(f"- Subdomains found: {len(domain_data.get('subdomains', []))}")
            
            whois = domain_data.get('whois', {})
            if 'registrar' in whois:
                summary_parts.append(f"- Registrar: {whois.get('registrar')}")
                summary_parts.append(f"- Creation date: {whois.get('creation_date')}")
        
        # Web intelligence
        if "web" in results:
            web_data = results["web"]
            summary_parts.append(f"\nWeb Intelligence:")
            summary_parts.append(f"- Technologies: {', '.join(web_data.get('technologies', []))}")
            
            security_headers = web_data.get('security_headers', {})
            if 'score' in security_headers:
                summary_parts.append(f"- Security headers score: {security_headers.get('score')} (Grade: {security_headers.get('grade')})")
            
            ssl_info = web_data.get('ssl_info', {})
            if 'not_after' in ssl_info:
                summary_parts.append(f"- SSL certificate expires: {ssl_info.get('not_after')}")
        
        # Network intelligence
        if "network" in results:
            network_data = results["network"]
            summary_parts.append(f"\nNetwork Intelligence:")
            open_ports = network_data.get('open_ports', [])
            summary_parts.append(f"- Open ports: {', '.join(map(str, open_ports))}")
            
            services = network_data.get('services', {})
            if services:
                summary_parts.append(f"- Services detected: {', '.join(services.values())}")
        
        # Social intelligence
        if "social" in results:
            social_data = results["social"]
            summary_parts.append(f"\nSocial Intelligence:")
            
            github = social_data.get('github', {})
            if github.get('organization'):
                org = github['organization']
                summary_parts.append(f"- GitHub organization: {org.get('name')} ({org.get('public_repos')} public repos)")
            
            profiles = social_data.get('social_profiles', {})
            active_profiles = [k for k, v in profiles.items() if v]
            if active_profiles:
                summary_parts.append(f"- Social profiles: {', '.join(active_profiles)}")
        
        # Threat intelligence
        if "threat" in results:
            threat_data = results["threat"]
            summary_parts.append(f"\nThreat Intelligence:")
            
            breach_check = threat_data.get('breach_check', {})
            if breach_check.get('total_breaches', 0) > 0:
                summary_parts.append(f"- Data breaches found: {breach_check.get('total_breaches')}")
            
            reputation = threat_data.get('reputation', {})
            if 'status' in reputation:
                summary_parts.append(f"- Reputation status: {reputation.get('status')}")
        
        return "\n".join(summary_parts)
    
    async def _generate_summary(self, target: str, intelligence_data: str) -> str:
        """Generate executive summary using LLM"""
        prompt = f"""As a cybersecurity analyst, provide a concise executive summary of the following OSINT reconnaissance results for target: {target}

Intelligence Data:
{intelligence_data}

Provide a 2-3 paragraph executive summary highlighting the most important findings and overall security posture."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert cybersecurity analyst specializing in OSINT and threat intelligence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    async def _calculate_risk_score(self, intelligence_data: str) -> int:
        """Calculate risk score using LLM analysis"""
        prompt = f"""Based on the following OSINT intelligence data, calculate a risk score from 0-100:

{intelligence_data}

Consider factors like:
- Open ports and exposed services
- Missing security headers
- SSL/TLS configuration
- Data breach history
- Attack surface size

Respond with ONLY a number between 0-100."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity risk assessment expert. Respond with only a number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            score_text = response.choices[0].message.content.strip()
            return int(score_text)
        except:
            return 50  # Default medium risk
    
    async def _analyze_attack_surface(self, intelligence_data: str) -> Dict[str, Any]:
        """Analyze attack surface using LLM"""
        prompt = f"""Analyze the attack surface based on this OSINT data:

{intelligence_data}

Identify:
1. External exposure points
2. Potential entry vectors
3. High-value targets

Respond in JSON format with keys: exposure_points, entry_vectors, high_value_targets"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a penetration testing expert. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)
        except:
            return {
                "exposure_points": ["Unable to analyze"],
                "entry_vectors": ["Unable to analyze"],
                "high_value_targets": ["Unable to analyze"]
            }
    
    async def _identify_vulnerabilities(self, intelligence_data: str) -> list:
        """Identify potential vulnerabilities using LLM"""
        prompt = f"""Based on this OSINT intelligence, identify potential security vulnerabilities:

{intelligence_data}

List specific vulnerabilities or security concerns. Format as JSON array with objects containing: title, severity, description"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a vulnerability assessment expert. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=600
            )
            
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)
        except:
            return [{"title": "Analysis Error", "severity": "Unknown", "description": "Unable to identify vulnerabilities"}]
    
    async def _generate_recommendations(self, target: str, intelligence_data: str) -> list:
        """Generate security recommendations using LLM"""
        prompt = f"""Based on the OSINT findings for {target}, provide actionable security recommendations:

{intelligence_data}

Provide 5-7 specific, actionable recommendations. Format as JSON array of strings."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a security consultant. Provide practical recommendations. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)
        except:
            return ["Unable to generate recommendations"]
    
    async def _find_correlations(self, intelligence_data: str) -> list:
        """Find correlations between different intelligence sources"""
        prompt = f"""Analyze this OSINT data and identify interesting correlations between different findings:

{intelligence_data}

Identify 3-5 notable correlations or patterns. Format as JSON array with objects containing: finding, significance"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an intelligence analyst expert at finding patterns. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)
        except:
            return [{"finding": "Analysis incomplete", "significance": "Unable to correlate data"}]

