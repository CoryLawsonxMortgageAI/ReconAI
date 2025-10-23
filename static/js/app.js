// ReconAI Frontend Application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize
    loadStats();
    loadRecentScans();
    
    // Form handlers
    const scanForm = document.getElementById('scanForm');
    const scanTypeSelect = document.getElementById('scanType');
    const moduleSelection = document.getElementById('moduleSelection');
    
    // Show/hide module selection based on scan type
    scanTypeSelect.addEventListener('change', function() {
        if (this.value === 'custom') {
            moduleSelection.style.display = 'block';
        } else {
            moduleSelection.style.display = 'none';
        }
    });
    
    // Handle form submission
    scanForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        await startScan();
    });
});

async function startScan() {
    const target = document.getElementById('target').value;
    const scanType = document.getElementById('scanType').value;
    const startBtn = document.getElementById('startScanBtn');
    const btnText = startBtn.querySelector('.btn-text');
    const btnLoader = startBtn.querySelector('.btn-loader');
    
    // Get selected modules
    let modules = ['domain', 'web', 'network', 'social', 'threat'];
    if (scanType === 'quick') {
        modules = ['domain', 'web'];
    } else if (scanType === 'custom') {
        modules = Array.from(document.querySelectorAll('input[name="modules"]:checked'))
            .map(cb => cb.value);
    }
    
    // Disable button and show loader
    startBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                target: target,
                scan_type: scanType,
                modules: modules
            })
        });
        
        if (!response.ok) {
            throw new Error('Scan failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
        // Refresh stats and recent scans
        loadStats();
        loadRecentScans();
        
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        // Re-enable button
        startBtn.disabled = false;
        btnText.style.display = 'inline-block';
        btnLoader.style.display = 'none';
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const scanResults = document.getElementById('scanResults');
    const aiAnalysis = document.getElementById('aiAnalysis');
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Display scan results
    let resultsHTML = '<div class="result-item">';
    resultsHTML += `<h3>Target: ${data.target}</h3>`;
    resultsHTML += `<p><strong>Scan ID:</strong> ${data.scan_id}</p>`;
    resultsHTML += `<p><strong>Status:</strong> <span class="status-completed">${data.status}</span></p>`;
    resultsHTML += `<p><strong>Timestamp:</strong> ${new Date(data.timestamp).toLocaleString()}</p>`;
    resultsHTML += '</div>';
    
    // Domain Intelligence
    if (data.results.domain) {
        resultsHTML += formatDomainResults(data.results.domain);
    }
    
    // Web Intelligence
    if (data.results.web) {
        resultsHTML += formatWebResults(data.results.web);
    }
    
    // Network Intelligence
    if (data.results.network) {
        resultsHTML += formatNetworkResults(data.results.network);
    }
    
    // Social Intelligence
    if (data.results.social) {
        resultsHTML += formatSocialResults(data.results.social);
    }
    
    // Threat Intelligence
    if (data.results.threat) {
        resultsHTML += formatThreatResults(data.results.threat);
    }
    
    scanResults.innerHTML = resultsHTML;
    
    // Display AI analysis
    aiAnalysis.innerHTML = formatAnalysis(data.analysis);
}

function formatDomainResults(domain) {
    let html = '<div class="result-item">';
    html += '<h3>🌐 Domain Intelligence</h3>';
    html += `<p><strong>IP Addresses:</strong> ${domain.ip_addresses.join(', ') || 'None'}</p>`;
    html += `<p><strong>Nameservers:</strong> ${domain.nameservers.join(', ') || 'None'}</p>`;
    html += `<p><strong>Subdomains Found:</strong> ${domain.subdomains.length}</p>`;
    
    if (domain.whois && domain.whois.registrar) {
        html += '<h4>WHOIS Information</h4>';
        html += `<p><strong>Registrar:</strong> ${domain.whois.registrar}</p>`;
        html += `<p><strong>Created:</strong> ${domain.whois.creation_date}</p>`;
        html += `<p><strong>Expires:</strong> ${domain.whois.expiration_date}</p>`;
    }
    
    html += '</div>';
    return html;
}

function formatWebResults(web) {
    let html = '<div class="result-item">';
    html += '<h3>🌍 Web Intelligence</h3>';
    html += `<p><strong>Technologies:</strong> ${web.technologies.join(', ') || 'None detected'}</p>`;
    
    if (web.security_headers && web.security_headers.score) {
        html += '<h4>Security Headers</h4>';
        html += `<p><strong>Score:</strong> ${web.security_headers.score} (Grade: ${web.security_headers.grade})</p>`;
    }
    
    if (web.ssl_info && web.ssl_info.not_after) {
        html += '<h4>SSL Certificate</h4>';
        html += `<p><strong>Expires:</strong> ${web.ssl_info.not_after}</p>`;
        html += `<p><strong>Protocol:</strong> ${web.ssl_info.protocol || 'N/A'}</p>`;
    }
    
    html += '</div>';
    return html;
}

function formatNetworkResults(network) {
    let html = '<div class="result-item">';
    html += '<h3>🔌 Network Intelligence</h3>';
    html += `<p><strong>IP Address:</strong> ${network.ip_address}</p>`;
    html += `<p><strong>Open Ports:</strong> ${network.open_ports.join(', ') || 'None'}</p>`;
    
    if (Object.keys(network.services).length > 0) {
        html += '<h4>Detected Services</h4>';
        for (const [port, service] of Object.entries(network.services)) {
            html += `<p>Port ${port}: ${service}</p>`;
        }
    }
    
    html += '</div>';
    return html;
}

function formatSocialResults(social) {
    let html = '<div class="result-item">';
    html += '<h3>👥 Social Intelligence</h3>';
    
    if (social.github && social.github.organization) {
        const org = social.github.organization;
        html += '<h4>GitHub Organization</h4>';
        html += `<p><strong>Name:</strong> ${org.name}</p>`;
        html += `<p><strong>Public Repos:</strong> ${org.public_repos}</p>`;
        html += `<p><strong>URL:</strong> <a href="${org.url}" target="_blank">${org.url}</a></p>`;
    }
    
    if (social.social_profiles) {
        html += '<h4>Social Profiles</h4>';
        for (const [platform, url] of Object.entries(social.social_profiles)) {
            if (url) {
                html += `<p><strong>${platform}:</strong> <a href="${url}" target="_blank">${url}</a></p>`;
            }
        }
    }
    
    html += '</div>';
    return html;
}

function formatThreatResults(threat) {
    let html = '<div class="result-item">';
    html += '<h3>⚠️ Threat Intelligence</h3>';
    
    if (threat.breach_check) {
        html += '<h4>Breach Check</h4>';
        html += `<p><strong>Breaches Found:</strong> ${threat.breach_check.total_breaches || 0}</p>`;
    }
    
    if (threat.reputation) {
        html += '<h4>Reputation</h4>';
        html += `<p><strong>Status:</strong> ${threat.reputation.status}</p>`;
        html += `<p><strong>Score:</strong> ${threat.reputation.score}</p>`;
    }
    
    html += '</div>';
    return html;
}

function formatAnalysis(analysis) {
    let html = '<div class="analysis-summary">';
    html += '<h3>📊 Executive Summary</h3>';
    html += `<p>${analysis.summary || 'No summary available'}</p>`;
    html += '</div>';
    
    // Risk Score
    let riskClass = 'risk-low';
    if (analysis.risk_score > 70) riskClass = 'risk-high';
    else if (analysis.risk_score > 40) riskClass = 'risk-medium';
    
    html += '<div class="result-item">';
    html += '<h3>🎯 Risk Assessment</h3>';
    html += `<p><strong>Risk Score:</strong> <span class="risk-score ${riskClass}">${analysis.risk_score}/100</span></p>`;
    html += '</div>';
    
    // Attack Surface
    if (analysis.attack_surface) {
        html += '<div class="result-item">';
        html += '<h3>🎯 Attack Surface</h3>';
        if (analysis.attack_surface.exposure_points) {
            html += '<h4>Exposure Points</h4><ul>';
            analysis.attack_surface.exposure_points.forEach(point => {
                html += `<li>${point}</li>`;
            });
            html += '</ul>';
        }
        html += '</div>';
    }
    
    // Vulnerabilities
    if (analysis.vulnerabilities && analysis.vulnerabilities.length > 0) {
        html += '<div class="result-item">';
        html += '<h3>🔓 Potential Vulnerabilities</h3>';
        analysis.vulnerabilities.forEach(vuln => {
            html += `<div class="vulnerability-item">`;
            html += `<h4>${vuln.title} <span style="color: var(--danger);">[${vuln.severity}]</span></h4>`;
            html += `<p>${vuln.description}</p>`;
            html += `</div>`;
        });
        html += '</div>';
    }
    
    // Recommendations
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        html += '<div class="result-item">';
        html += '<h3>💡 Recommendations</h3>';
        analysis.recommendations.forEach(rec => {
            html += `<div class="recommendation-item">${rec}</div>`;
        });
        html += '</div>';
    }
    
    return html;
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('totalScans').textContent = stats.total_scans || 0;
        document.getElementById('completedScans').textContent = stats.completed_scans || 0;
        document.getElementById('totalFindings').textContent = stats.total_findings || 0;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

async function loadRecentScans() {
    try {
        const response = await fetch('/api/scans?limit=5');
        const data = await response.json();
        const scansList = document.getElementById('recentScansList');
        
        if (data.scans && data.scans.length > 0) {
            let html = '';
            data.scans.forEach(scan => {
                html += '<div class="scan-item">';
                html += `<div>`;
                html += `<strong>${scan.target}</strong><br>`;
                html += `<small>${new Date(scan.created_at).toLocaleString()}</small>`;
                html += `</div>`;
                html += `<span class="scan-status status-${scan.status}">${scan.status}</span>`;
                html += '</div>';
            });
            scansList.innerHTML = html;
        } else {
            scansList.innerHTML = '<p style="color: var(--text-secondary);">No scans yet</p>';
        }
    } catch (error) {
        console.error('Failed to load recent scans:', error);
    }
}

