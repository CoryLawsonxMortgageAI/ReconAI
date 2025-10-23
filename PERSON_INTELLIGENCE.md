# Person Intelligence Module - Documentation

## Overview

The Person Intelligence module extends ReconAI with comprehensive background check and person investigation capabilities. It gathers publicly available information about individuals from various legitimate sources including criminal records, court cases, professional licenses, social media, and public records.

## Features

### 1. Criminal Records Search

**Sources:**
- National Sex Offender Public Website (NSOPW)
- Federal Bureau of Prisons (BOP) Inmate Locator
- State criminal databases (where publicly accessible)
- County sheriff's offices
- State departments of corrections

**Data Gathered:**
- Federal criminal records
- State-level criminal history
- Sex offender registration status
- Current incarceration status
- Historical arrests and convictions

### 2. Court Records Search

**Sources:**
- PACER (Federal court records)
- State court systems
- County clerk of court offices
- Municipal court records

**Types of Cases:**
- Criminal cases (felonies and misdemeanors)
- Civil litigation
- Traffic violations
- Small claims
- Bankruptcy filings
- Family court matters (where public)

### 3. Professional Information

**Sources:**
- LinkedIn profiles
- State professional licensing boards
- Medical board databases
- State bar associations
- Professional certification bodies

**Data Gathered:**
- Employment history
- Professional licenses (doctors, lawyers, nurses, etc.)
- Professional certifications
- Educational background
- Publications and patents

### 4. Social Media Intelligence

**Platforms:**
- Facebook
- Twitter/X
- Instagram
- TikTok
- YouTube
- LinkedIn

**Data Gathered:**
- Public profiles
- Posts and content
- Connections and networks
- Location information
- Interests and affiliations

### 5. Public Records

**Types:**
- Voter registration (public in many states)
- Property ownership records
- Business registrations
- Corporate filings
- Marriage and divorce records
- Birth and death records (where accessible)

### 6. Additional Intelligence

**Sources:**
- County property appraiser offices
- Secretary of State business divisions
- SEC EDGAR database (for executives)
- Professional association directories
- Academic institution records

## Usage

### API Endpoint

```bash
POST /api/scan
Content-Type: application/json

{
  "target": "John Smith",
  "target_type": "person",
  "state": "CA",
  "dob": "1980-01-15",
  "scan_type": "full"
}
```

### Python Example

```python
import asyncio
from modules.person_intel import PersonIntelligence

async def run_person_scan():
    person_intel = PersonIntelligence()
    
    results = await person_intel.scan(
        person_name="John Smith",
        state="CA",
        dob="1980-01-15"
    )
    
    print(results)

asyncio.run(run_person_scan())
```

### Web Interface

1. Navigate to ReconAI dashboard
2. Select "Person / Individual" from Target Type dropdown
3. Enter full name
4. Optionally specify state and date of birth for more accurate results
5. Click "Start Reconnaissance"

## Data Sources by State

### Criminal Records

Each state maintains its own criminal records system:

| State | System | Public Access |
|-------|--------|---------------|
| California | DOJ Criminal Records | Limited |
| New York | DCJS | Limited |
| Texas | DPS Crime Records | Limited |
| Florida | FDLE | Public portal available |
| Illinois | ISP | Limited |

**Note:** Most states require official background check requests for complete criminal history.

### Court Records

| State | System | Online Access |
|-------|--------|---------------|
| California | California Courts | Yes (limited) |
| New York | NY Courts | Yes (limited) |
| Texas | Texas Courts | Yes (varies by county) |
| Florida | Florida Courts | Yes (extensive) |
| Illinois | Illinois Courts | Yes (limited) |

### Professional Licenses

| Profession | Database | Access |
|------------|----------|--------|
| Medical | State Medical Boards | Public |
| Legal | State Bar Associations | Public |
| Nursing | State Nursing Boards | Public |
| Real Estate | State RE Commissions | Public |
| Contractors | State Contractor Boards | Public |

## Legal and Ethical Considerations

### Authorized Use Cases

✅ **Permitted Uses:**
- Pre-employment background checks (with consent)
- Tenant screening (with consent)
- Due diligence investigations
- Legal proceedings and discovery
- Fraud investigations
- Missing persons investigations
- Genealogical research
- Academic research

### Prohibited Uses

❌ **NOT Permitted:**
- Stalking or harassment
- Identity theft
- Discrimination in employment or housing
- Unauthorized credit decisions
- Invasion of privacy
- Doxxing or public shaming

### Legal Compliance

**Fair Credit Reporting Act (FCRA):**
- If used for employment, housing, or credit decisions, must comply with FCRA
- Requires subject's written consent
- Must provide adverse action notices
- Must use FCRA-compliant background check providers

**State Privacy Laws:**
- California Consumer Privacy Act (CCPA)
- Virginia Consumer Data Protection Act (VCDPA)
- Colorado Privacy Act (CPA)
- Other state-specific privacy regulations

**Driver's Privacy Protection Act (DPPA):**
- Restricts use of DMV records
- Requires permissible purpose

**Computer Fraud and Abuse Act (CFAA):**
- Prohibits unauthorized access to computer systems
- Only access publicly available information

## Data Accuracy and Limitations

### Accuracy Considerations

- **Name Matching:** Common names may return multiple results
- **Date of Birth:** Helps narrow results but not always available
- **State:** Limits search scope but person may have records in multiple states
- **Timeliness:** Some records may be outdated or incomplete

### Known Limitations

1. **Sealed Records:** Juvenile records and sealed cases are not accessible
2. **Expunged Records:** Legally expunged records should not appear
3. **Private Records:** Medical records, financial records, and other private information are not accessible
4. **Interstate Gaps:** Records from multiple states may not be consolidated
5. **Name Changes:** May miss records under previous names

## Best Practices

### 1. Verify Identity

- Use multiple data points (name, DOB, state, city)
- Cross-reference results across multiple sources
- Confirm identity before making decisions

### 2. Respect Privacy

- Only gather information necessary for your purpose
- Secure all collected data
- Delete data when no longer needed
- Follow data retention policies

### 3. Legal Compliance

- Obtain proper consent when required
- Use FCRA-compliant providers for regulated purposes
- Provide required disclosures
- Follow adverse action procedures

### 4. Data Validation

- Verify critical information through official sources
- Don't rely solely on aggregated data
- Check dates and jurisdictions
- Look for inconsistencies

## Integration with Existing Systems

### Background Check Services

For comprehensive background checks, integrate with:

- **Checkr** - Employment screening
- **GoodHire** - Background checks
- **Sterling** - Enterprise screening
- **HireRight** - Pre-employment screening

### Public Records APIs

- **LexisNexis** - Comprehensive public records
- **TLO** - Investigation and research
- **CLEAR** - Law enforcement and investigations
- **Accurint** - Skip tracing and investigations

### Court Records APIs

- **CourtListener** - Federal and state court opinions
- **PACER** - Federal court records
- **State-specific APIs** - Varies by jurisdiction

## Output Format

### Person Intelligence Report Structure

```json
{
  "target": "John Smith",
  "state": "CA",
  "dob": "1980-01-15",
  "timestamp": "2025-10-23T02:00:00Z",
  "identity": {
    "parsed_name": {
      "first_name": "John",
      "middle_name": "",
      "last_name": "Smith",
      "suffix": ""
    }
  },
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
```

## Troubleshooting

### Common Issues

**Issue:** No results found
- **Solution:** Try variations of the name, check spelling, expand search to adjacent states

**Issue:** Too many results
- **Solution:** Add more identifying information (DOB, state, city), use middle name or initial

**Issue:** Outdated information
- **Solution:** Check directly with official sources for most current data

**Issue:** Access denied
- **Solution:** Some records require official requests or subscriptions

## Support and Resources

### Official Resources

- **NSOPW:** https://www.nsopw.gov
- **PACER:** https://pacer.uscourts.gov
- **BOP Inmate Locator:** https://www.bop.gov/inmateloc/
- **State Court Systems:** Varies by state

### Legal Resources

- **FCRA Compliance:** https://www.ftc.gov/enforcement/statutes/fair-credit-reporting-act
- **EEOC Guidance:** https://www.eeoc.gov/laws/guidance
- **State Privacy Laws:** Consult state attorney general websites

## Disclaimer

This tool is provided for authorized investigative and research purposes only. Users are responsible for ensuring their use complies with all applicable federal, state, and local laws. The developers assume no liability for misuse or unauthorized use of this tool.

**Always:**
- Obtain proper authorization
- Follow legal requirements
- Respect privacy rights
- Use data responsibly
- Verify critical information

## Version History

- **v2.0.0** - Initial person intelligence module
  - Criminal records search
  - Court records search
  - Professional information
  - Social media intelligence
  - Public records search
  - Property and business records

## Future Enhancements

- Integration with commercial background check APIs
- Automated identity verification
- Multi-state consolidated searches
- Real-time monitoring and alerts
- Enhanced name matching algorithms
- Relationship mapping and visualization

