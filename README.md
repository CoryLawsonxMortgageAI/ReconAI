> [!WARNING]
> This tool is intended for authorized security testing and educational purposes only. Unauthorized use of this software for reconnaissance or any other purpose against systems you do not have explicit permission to test is illegal and strictly prohibited. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

# ReconAI - Autonomous OSINT Intelligence Platform

**ReconAI** is a comprehensive, AI-powered Open Source Intelligence (OSINT) platform designed for defensive security teams, red teamers, and cybersecurity researchers. It automates the process of gathering and correlating publicly available information to map an organization's external attack surface, identify potential threats, and provide actionable security insights. By integrating a powerful Large Language Model (LLM), ReconAI transforms raw data into strategic intelligence, enabling proactive defense and informed security testing.

This project was inspired by the need for a modern, easy-to-use reconnaissance tool that leverages the analytical power of AI to cut through the noise of OSINT data. Unlike traditional tools that present raw data, ReconAI provides correlated analysis, risk scoring, and prioritized recommendations, helping security professionals focus on what matters most.

## Key Features

ReconAI offers a suite of features designed to streamline the OSINT process from start to finish. The platform is built around a modular architecture that allows for flexible and scalable reconnaissance operations.

| Feature | Description |
| :--- | :--- |
| **Modular Reconnaissance** | Includes modules for Domain, Web, Network, Social, and Threat Intelligence, allowing for targeted or comprehensive scans. |
| **AI-Powered Analysis** | Utilizes a cutting-edge LLM (GPT-4) to analyze, correlate, and summarize findings, providing an executive-level overview of the target's security posture. |
| **Comprehensive Reporting** | Generates detailed reports that include an executive summary, risk score, attack surface analysis, identified vulnerabilities, and actionable recommendations. |
| **Web-Based Interface** | A clean, professional web UI with a black and silver theme allows for easy scan management and visualization of results. |
| **RESTful API** | Provides a full-featured API for programmatic access, enabling integration with other security tools and automated workflows. |
| **Ethical & Safe** | Designed with safety in mind, incorporating rate limiting and adherence to `robots.txt` to ensure responsible use. |
| **SQLite Backend** | All scan data is stored locally in a SQLite database, ensuring data privacy and allowing for historical analysis. |

## Technology Stack

The platform is built on a modern, robust technology stack, prioritizing performance, scalability, and ease of development.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | For building a high-performance RESTful API and serving the web interface. |
| **LLM Integration** | [OpenAI API](https://platform.openai.com/docs/api-reference) | Powers the AI analysis engine for summarizing and correlating intelligence data. |
| **Database** | [SQLite](https://www.sqlite.org/index.html) | Provides a lightweight, file-based database for storing scan results and application data. |
| **OSINT Libraries** | `dnspython`, `python-whois`, `aiohttp` | A collection of specialized Python libraries for gathering OSINT data. |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | A simple yet effective frontend stack for the user interface, with no complex framework dependencies. |
| **Deployment** | [Uvicorn](https://www.uvicorn.org/) | An ASGI server for running the FastAPI application. |

## Installation & Usage

Getting started with ReconAI is straightforward. The following steps will guide you through setting up the application and running your first scan.

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ReconAI.git
    cd ReconAI
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your OpenAI API key:**

    Create a `.env` file in the root directory and add your API key:

    ```
    OPENAI_API_KEY=your-api-key-here
    ```

### Running the Application

To start the ReconAI server, run the following command from the root directory:

```bash
python3 app.py
```

The application will be accessible at `http://localhost:8000`.

## API Documentation

ReconAI provides a RESTful API for programmatic interaction. The API is automatically documented using Swagger UI and can be accessed at `http://localhost:8000/docs` when the application is running.

### Main Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/scan` | `POST` | Start a new reconnaissance scan. |
| `/api/scans` | `GET` | Retrieve a list of recent scans. |
| `/api/scan/{scan_id}` | `GET` | Get the detailed results of a specific scan. |
| `/api/health` | `GET` | Check the health status of the application. |

### Example: Starting a Scan

```bash
curl -X 'POST' \
  'http://localhost:8000/api/scan' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "target": "example.com",
    "scan_type": "quick"
  }'
```

## Contributing

Contributions from the community are welcome! Whether it's adding new modules, improving the UI, or fixing bugs, your help is appreciated. Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

ReconAI is built upon the work of the incredible open-source community. We extend our gratitude to the developers of the following projects and libraries, without which this tool would not be possible:

- [SpiderFoot](https://github.com/smicallef/spiderfoot) for inspiration and for being a titan in the OSINT community.
- The creators of the numerous Python libraries that power our reconnaissance modules.
- The open-source intelligence community for their continuous innovation and sharing of knowledge.

