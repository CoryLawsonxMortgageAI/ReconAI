"""
Database module for ReconAI
Handles data persistence and retrieval
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional


class Database:
    """SQLite database handler for ReconAI"""
    
    def __init__(self, db_path: str = "data/reconai.db"):
        self.db_path = db_path
        self.conn = None
    
    def initialize(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Create scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                scan_id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                results TEXT,
                analysis TEXT
            )
        """)
        
        # Create findings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                scan_id TEXT NOT NULL,
                module TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            )
        """)
        
        # Create statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_scans INTEGER DEFAULT 0,
                total_findings INTEGER DEFAULT 0,
                last_updated TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
        print("[+] Database initialized successfully")
    
    def create_scan(self, target: str, scan_type: str) -> str:
        """Create a new scan entry"""
        scan_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO scans (scan_id, target, scan_type, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (scan_id, target, scan_type, "running", datetime.utcnow().isoformat()))
        
        self.conn.commit()
        return scan_id
    
    def save_results(self, scan_id: str, results: Dict[str, Any], analysis: Dict[str, Any]):
        """Save scan results and analysis"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE scans
            SET status = ?, completed_at = ?, results = ?, analysis = ?
            WHERE scan_id = ?
        """, (
            "completed",
            datetime.utcnow().isoformat(),
            json.dumps(results),
            json.dumps(analysis),
            scan_id
        ))
        
        self.conn.commit()
    
    def get_scan(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve scan by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM scans WHERE scan_id = ?", (scan_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "scan_id": row["scan_id"],
                "target": row["target"],
                "scan_type": row["scan_type"],
                "status": row["status"],
                "created_at": row["created_at"],
                "completed_at": row["completed_at"],
                "results": json.loads(row["results"]) if row["results"] else {},
                "analysis": json.loads(row["analysis"]) if row["analysis"] else {}
            }
        return None
    
    def get_recent_scans(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scans"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT scan_id, target, scan_type, status, created_at, completed_at
            FROM scans
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics"""
        cursor = self.conn.cursor()
        
        # Total scans
        cursor.execute("SELECT COUNT(*) as count FROM scans")
        total_scans = cursor.fetchone()["count"]
        
        # Completed scans
        cursor.execute("SELECT COUNT(*) as count FROM scans WHERE status = 'completed'")
        completed_scans = cursor.fetchone()["count"]
        
        # Total findings
        cursor.execute("SELECT COUNT(*) as count FROM findings")
        total_findings = cursor.fetchone()["count"]
        
        return {
            "total_scans": total_scans,
            "completed_scans": completed_scans,
            "total_findings": total_findings,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

