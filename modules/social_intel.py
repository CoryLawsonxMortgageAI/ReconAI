"""
Social Intelligence Module
Gathers public information from social platforms and code repositories
"""

import aiohttp
from typing import Dict, Any
from datetime import datetime


class SocialIntelligence:
    """Social media and public profile reconnaissance module"""
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=10)
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """
        Perform social intelligence gathering
        
        Args:
            target: Domain or organization name
            
        Returns:
            Dictionary containing social intelligence
        """
        results = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "github": {},
            "social_profiles": {},
            "public_mentions": []
        }
        
        # Extract organization name from domain
        org_name = target.split('.')[0] if '.' in target else target
        
        # GitHub reconnaissance
        results["github"] = await self._scan_github(org_name)
        
        # Check common social media profiles
        results["social_profiles"] = await self._check_social_profiles(org_name)
        
        return results
    
    async def _scan_github(self, org_name: str) -> Dict[str, Any]:
        """Scan GitHub for organization or user"""
        github_data = {
            "organization": None,
            "repositories": [],
            "users": []
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            # Check for organization
            try:
                async with session.get(
                    f"https://api.github.com/orgs/{org_name}",
                    headers={"Accept": "application/vnd.github.v3+json"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        github_data["organization"] = {
                            "name": data.get("name"),
                            "login": data.get("login"),
                            "description": data.get("description"),
                            "public_repos": data.get("public_repos"),
                            "followers": data.get("followers"),
                            "created_at": data.get("created_at"),
                            "url": data.get("html_url")
                        }
                        
                        # Get public repositories
                        try:
                            async with session.get(
                                f"https://api.github.com/orgs/{org_name}/repos",
                                headers={"Accept": "application/vnd.github.v3+json"}
                            ) as repo_response:
                                if repo_response.status == 200:
                                    repos = await repo_response.json()
                                    github_data["repositories"] = [
                                        {
                                            "name": repo.get("name"),
                                            "description": repo.get("description"),
                                            "language": repo.get("language"),
                                            "stars": repo.get("stargazers_count"),
                                            "forks": repo.get("forks_count"),
                                            "url": repo.get("html_url")
                                        }
                                        for repo in repos[:10]  # Limit to 10 repos
                                    ]
                        except:
                            pass
            except:
                # Try as user instead
                try:
                    async with session.get(
                        f"https://api.github.com/users/{org_name}",
                        headers={"Accept": "application/vnd.github.v3+json"}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            github_data["users"].append({
                                "login": data.get("login"),
                                "name": data.get("name"),
                                "bio": data.get("bio"),
                                "public_repos": data.get("public_repos"),
                                "followers": data.get("followers"),
                                "url": data.get("html_url")
                            })
                except:
                    pass
        
        return github_data
    
    async def _check_social_profiles(self, org_name: str) -> Dict[str, Any]:
        """Check for social media profiles"""
        profiles = {
            "twitter": None,
            "linkedin": None,
            "facebook": None
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            # Check Twitter/X
            try:
                async with session.get(f"https://twitter.com/{org_name}") as response:
                    if response.status == 200:
                        profiles["twitter"] = f"https://twitter.com/{org_name}"
            except:
                pass
            
            # Check LinkedIn
            try:
                async with session.get(f"https://www.linkedin.com/company/{org_name}") as response:
                    if response.status == 200:
                        profiles["linkedin"] = f"https://www.linkedin.com/company/{org_name}"
            except:
                pass
            
            # Check Facebook
            try:
                async with session.get(f"https://www.facebook.com/{org_name}") as response:
                    if response.status == 200:
                        profiles["facebook"] = f"https://www.facebook.com/{org_name}"
            except:
                pass
        
        return profiles

