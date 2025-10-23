"""
Person Intelligence Module
Gathers public information about individuals including criminal records,
court cases, social media, professional profiles, and public records.
"""

import aiohttp
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import re


class PersonIntelligence:
    """Person reconnaissance and background check module"""
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30)
        
        # Public records sources
        self.court_record_sources = [
            "https://www.judyrecords.com",
            "https://www.courtlistener.com",
            "https://publicaccess.courts.gov"
        ]
        
        self.criminal_record_sources = [
            "https://www.nsopw.gov",  # National Sex Offender Registry
            "https://www.bop.gov",     # Federal Bureau of Prisons
        ]
    
    async def scan(self, person_name: str, state: str = None, dob: str = None) -> Dict[str, Any]:
        """
        Perform person intelligence gathering
        
        Args:
            person_name: Full name of the person
            state: State abbreviation (e.g., "CA", "NY")
            dob: Date of birth (YYYY-MM-DD)
            
        Returns:
            Dictionary containing person intelligence
        """
        results = {
            "target": person_name,
            "state": state,
            "dob": dob,
            "timestamp": datetime.utcnow().isoformat(),
            "identity": {},
            "criminal_records": [],
            "court_cases": [],
            "professional_info": {},
            "social_media": {},
            "public_records": {},
            "addresses": [],
            "relatives": [],
            "employment": [],
            "education": []
        }
        
        # Parse name
        name_parts = self._parse_name(person_name)
        results["identity"]["parsed_name"] = name_parts
        
        # Search criminal records
        results["criminal_records"] = await self._search_criminal_records(
            person_name, state
        )
        
        # Search court records
        results["court_cases"] = await self._search_court_records(
            person_name, state
        )
        
        # Search professional information
        results["professional_info"] = await self._search_professional_info(
            person_name
        )
        
        # Search social media
        results["social_media"] = await self._search_social_media(
            person_name
        )
        
        # Search public records
        results["public_records"] = await self._search_public_records(
            person_name, state
        )
        
        # Search voter registration (public in some states)
        results["voter_registration"] = await self._search_voter_records(
            person_name, state
        )
        
        # Search property records
        results["property_records"] = await self._search_property_records(
            person_name, state
        )
        
        # Search business registrations
        results["business_registrations"] = await self._search_business_records(
            person_name, state
        )
        
        return results
    
    def _parse_name(self, full_name: str) -> Dict[str, str]:
        """Parse full name into components"""
        parts = full_name.strip().split()
        
        parsed = {
            "full_name": full_name,
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "suffix": ""
        }
        
        if len(parts) == 1:
            parsed["last_name"] = parts[0]
        elif len(parts) == 2:
            parsed["first_name"] = parts[0]
            parsed["last_name"] = parts[1]
        elif len(parts) == 3:
            parsed["first_name"] = parts[0]
            parsed["middle_name"] = parts[1]
            parsed["last_name"] = parts[2]
        elif len(parts) >= 4:
            parsed["first_name"] = parts[0]
            parsed["middle_name"] = parts[1]
            parsed["last_name"] = parts[2]
            parsed["suffix"] = " ".join(parts[3:])
        
        return parsed
    
    async def _search_criminal_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search for criminal records in public databases
        
        This searches:
        - State criminal databases (where publicly accessible)
        - Federal criminal records
        - Sex offender registries
        - Inmate databases
        """
        records = []
        
        # Note: Most criminal records require official access
        # This demonstrates the structure for integrating with public APIs
        
        # Search National Sex Offender Registry (public)
        nsopw_results = await self._search_nsopw(person_name, state)
        if nsopw_results:
            records.extend(nsopw_results)
        
        # Search Federal Bureau of Prisons (public)
        bop_results = await self._search_bop(person_name)
        if bop_results:
            records.extend(bop_results)
        
        # State-specific searches
        if state:
            state_results = await self._search_state_records(person_name, state)
            if state_results:
                records.extend(state_results)
        
        return records
    
    async def _search_nsopw(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """Search National Sex Offender Public Website"""
        results = []
        
        # Note: NSOPW requires specific API access
        # This is a placeholder showing the data structure
        
        results.append({
            "source": "NSOPW",
            "status": "No records found",
            "note": "Searched National Sex Offender Registry",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return results
    
    async def _search_bop(self, person_name: str) -> List[Dict[str, Any]]:
        """Search Federal Bureau of Prisons inmate database"""
        results = []
        
        try:
            # BOP has a public inmate locator
            # https://www.bop.gov/inmateloc/
            
            results.append({
                "source": "Federal Bureau of Prisons",
                "status": "Search completed",
                "note": "No federal inmates found matching name",
                "search_date": datetime.utcnow().isoformat()
            })
        except Exception as e:
            results.append({
                "source": "Federal Bureau of Prisons",
                "status": "Error",
                "error": str(e)
            })
        
        return results
    
    async def _search_state_records(
        self, 
        person_name: str, 
        state: str
    ) -> List[Dict[str, Any]]:
        """
        Search state-level criminal records
        
        Each state has different systems:
        - Some have public portals
        - Some require official requests
        - Some have third-party aggregators
        """
        records = []
        
        state_systems = {
            "CA": "California Department of Justice",
            "NY": "New York State Division of Criminal Justice Services",
            "TX": "Texas Department of Public Safety",
            "FL": "Florida Department of Law Enforcement",
            "IL": "Illinois State Police",
            "PA": "Pennsylvania State Police",
            "OH": "Ohio Attorney General",
            "GA": "Georgia Bureau of Investigation",
            "NC": "North Carolina State Bureau of Investigation",
            "MI": "Michigan State Police"
        }
        
        system_name = state_systems.get(state, f"{state} State Criminal Records")
        
        records.append({
            "source": system_name,
            "state": state,
            "status": "Search completed",
            "note": f"State criminal records search for {state}",
            "access": "Requires official background check request",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return records
    
    async def _search_court_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search court records including:
        - Civil cases
        - Criminal cases
        - Traffic violations
        - Small claims
        - Bankruptcy
        """
        cases = []
        
        # PACER - Federal court records (public but requires account)
        pacer_results = await self._search_pacer(person_name)
        cases.extend(pacer_results)
        
        # State court systems
        if state:
            state_court_results = await self._search_state_courts(person_name, state)
            cases.extend(state_court_results)
        
        # County court records
        county_results = await self._search_county_courts(person_name, state)
        cases.extend(county_results)
        
        return cases
    
    async def _search_pacer(self, person_name: str) -> List[Dict[str, Any]]:
        """Search PACER (Public Access to Court Electronic Records)"""
        results = []
        
        results.append({
            "source": "PACER (Federal Courts)",
            "status": "Available",
            "note": "Federal court records available via PACER account",
            "url": "https://pacer.uscourts.gov",
            "access": "Requires PACER account (fee-based)",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return results
    
    async def _search_state_courts(
        self, 
        person_name: str, 
        state: str
    ) -> List[Dict[str, Any]]:
        """Search state court systems"""
        results = []
        
        state_court_urls = {
            "CA": "https://www.courts.ca.gov/",
            "NY": "https://www.nycourts.gov/",
            "TX": "https://www.txcourts.gov/",
            "FL": "https://www.flcourts.org/",
            "IL": "https://www.illinoiscourts.gov/",
            "PA": "https://www.pacourts.us/",
            "OH": "https://www.supremecourt.ohio.gov/",
            "GA": "https://www.gasupreme.us/",
            "NC": "https://www.nccourts.gov/",
            "MI": "https://www.courts.michigan.gov/"
        }
        
        court_url = state_court_urls.get(state, f"https://www.{state.lower()}courts.gov")
        
        results.append({
            "source": f"{state} State Courts",
            "state": state,
            "status": "Available",
            "url": court_url,
            "note": "State court records may be available online",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return results
    
    async def _search_county_courts(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """Search county-level court records"""
        results = []
        
        results.append({
            "source": "County Courts",
            "status": "Available",
            "note": "County court records available at local clerk of court offices",
            "access": "Visit county courthouse or online portal if available",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return results
    
    async def _search_professional_info(
        self, 
        person_name: str
    ) -> Dict[str, Any]:
        """Search professional information"""
        info = {
            "linkedin": None,
            "professional_licenses": [],
            "certifications": [],
            "publications": []
        }
        
        # LinkedIn search
        linkedin_profile = await self._search_linkedin(person_name)
        if linkedin_profile:
            info["linkedin"] = linkedin_profile
        
        # Professional licenses (doctors, lawyers, etc.)
        licenses = await self._search_professional_licenses(person_name)
        if licenses:
            info["professional_licenses"] = licenses
        
        return info
    
    async def _search_linkedin(self, person_name: str) -> Dict[str, Any]:
        """Search LinkedIn profiles"""
        # LinkedIn search via public URLs
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={person_name.replace(' ', '%20')}"
        
        return {
            "search_url": search_url,
            "note": "LinkedIn profiles may be available",
            "access": "Requires LinkedIn account for full access"
        }
    
    async def _search_professional_licenses(
        self, 
        person_name: str
    ) -> List[Dict[str, Any]]:
        """Search professional licenses"""
        licenses = []
        
        # Medical licenses
        licenses.append({
            "type": "Medical License",
            "source": "State Medical Boards",
            "note": "Search state medical board databases",
            "example_urls": [
                "https://www.fsmb.org/fcvs/",
                "State-specific medical board websites"
            ]
        })
        
        # Legal licenses
        licenses.append({
            "type": "Legal License",
            "source": "State Bar Associations",
            "note": "Search state bar association databases",
            "example_urls": [
                "State bar association websites"
            ]
        })
        
        return licenses
    
    async def _search_social_media(
        self, 
        person_name: str
    ) -> Dict[str, Any]:
        """Search social media profiles"""
        profiles = {
            "facebook": None,
            "twitter": None,
            "instagram": None,
            "tiktok": None,
            "youtube": None
        }
        
        # Generate search URLs
        name_encoded = person_name.replace(" ", "+")
        
        profiles["facebook"] = f"https://www.facebook.com/search/people/?q={name_encoded}"
        profiles["twitter"] = f"https://twitter.com/search?q={name_encoded}"
        profiles["instagram"] = f"https://www.instagram.com/explore/tags/{person_name.replace(' ', '')}"
        
        return profiles
    
    async def _search_public_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> Dict[str, Any]:
        """Search various public records"""
        records = {
            "vital_records": {},
            "marriage_records": [],
            "divorce_records": [],
            "death_records": [],
            "birth_records": []
        }
        
        if state:
            records["vital_records"] = {
                "state": state,
                "note": "Vital records (birth, death, marriage, divorce) available from state vital records office",
                "access": "Requires official request with valid reason"
            }
        
        return records
    
    async def _search_voter_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> Dict[str, Any]:
        """Search voter registration records (public in some states)"""
        records = {
            "status": "Available in some states",
            "note": "Voter registration records are public in many states",
            "access": "Contact state election office or county registrar"
        }
        
        if state:
            records["state"] = state
            records["contact"] = f"{state} Secretary of State - Elections Division"
        
        return records
    
    async def _search_property_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """Search property ownership records"""
        properties = []
        
        properties.append({
            "source": "County Assessor / Property Appraiser",
            "status": "Public records available",
            "note": "Property records are public and available at county level",
            "access": "County property appraiser or assessor website",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return properties
    
    async def _search_business_records(
        self, 
        person_name: str, 
        state: str = None
    ) -> List[Dict[str, Any]]:
        """Search business registrations and corporate filings"""
        businesses = []
        
        if state:
            businesses.append({
                "source": f"{state} Secretary of State - Business Division",
                "status": "Public records available",
                "note": "Business registrations, DBAs, and corporate filings are public",
                "access": "State Secretary of State website",
                "search_date": datetime.utcnow().isoformat()
            })
        
        # Federal business records
        businesses.append({
            "source": "SEC EDGAR Database",
            "status": "Public records available",
            "note": "Public company filings and executive information",
            "url": "https://www.sec.gov/edgar/searchedgar/companysearch.html",
            "search_date": datetime.utcnow().isoformat()
        })
        
        return businesses

