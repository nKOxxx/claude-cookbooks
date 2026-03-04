#!/usr/bin/env python3
"""
AgentVault Example: Secure Agent Credential Management

This script demonstrates how to use AgentVault for secure credential
management between AI agents, including:
- Creating encrypted vaults
- Storing and retrieving credentials
- Sharing credentials between agents
- Receiving shared credentials
- Audit logging

Requirements:
    pip install agentvault

Author: AgentVault Contributors
License: MIT
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List


# =============================================================================
# Mock AgentVault Implementation (for demonstration)
# In production, use: from agentvault import Vault, Credential, etc.
# =============================================================================

class Credential:
    """Represents a stored credential with metadata."""
    
    def __init__(self, name: str, value: str, metadata: Optional[Dict] = None):
        self.name = name
        self.value = value
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()
        self.last_accessed = None
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed
        }


class AuditLogEntry:
    """Represents a single audit log entry."""
    
    def __init__(self, action: str, credential_name: str, agent_id: str, 
                 timestamp: Optional[str] = None, details: Optional[Dict] = None):
        self.action = action
        self.credential_name = credential_name
        self.agent_id = agent_id
        self.timestamp = timestamp or datetime.now().isoformat()
        self.details = details or {}
    
    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "credential_name": self.credential_name,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "details": self.details
        }


class Vault:
    """
    Secure vault for storing and managing credentials.
    
    In production, this would use actual encryption (AES-256-GCM, etc.)
    and secure storage backends.
    """
    
    def __init__(self, encryption_key: str, vault_name: str = "default"):
        self.vault_name = vault_name
        self.encryption_key = encryption_key
        self._credentials: Dict[str, Credential] = {}
        self._audit_logs: List[AuditLogEntry] = []
        self._sharing_policies: Dict[str, Dict] = {}
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the vault."""
        print(f"🔐 Initializing vault: {self.vault_name}")
        print(f"   Encryption: AES-256-GCM (simulated)")
        self._initialized = True
        self._log_action("VAULT_INITIALIZED", "", "admin")
    
    def _log_action(self, action: str, credential_name: str, agent_id: str, 
                    details: Optional[Dict] = None) -> None:
        """Log an action to the audit trail."""
        entry = AuditLogEntry(action, credential_name, agent_id, details=details)
        self._audit_logs.append(entry)
    
    def store_credential(self, credential: Credential, agent_id: str = "admin") -> None:
        """Store a credential in the vault."""
        if not self._initialized:
            raise RuntimeError("Vault not initialized. Call initialize() first.")
        
        self._credentials[credential.name] = credential
        self._log_action("STORE", credential.name, agent_id, 
                        {"metadata": credential.metadata})
        print(f"✅ Stored credential: {credential.name}")
    
    def get_credential(self, name: str, agent_id: str = "admin") -> Optional[Credential]:
        """Retrieve a credential from the vault."""
        if not self._initialized:
            raise RuntimeError("Vault not initialized. Call initialize() first.")
        
        credential = self._credentials.get(name)
        if credential:
            credential.last_accessed = datetime.now().isoformat()
            self._log_action("RETRIEVE", name, agent_id)
            print(f"📤 Retrieved credential: {name}")
            return credential
        else:
            self._log_action("RETRIEVE_FAILED", name, agent_id, {"reason": "not_found"})
            print(f"❌ Credential not found: {name}")
            return None
    
    def list_credentials(self, agent_id: str = "admin") -> List[str]:
        """List all credential names in the vault."""
        self._log_action("LIST", "", agent_id, {"count": len(self._credentials)})
        return list(self._credentials.keys())
    
    def share_credential(self, credential_name: str, target_agent: str, 
                         permissions: List[str], agent_id: str = "admin") -> bool:
        """Share a credential with another agent."""
        if credential_name not in self._credentials:
            print(f"❌ Cannot share - credential not found: {credential_name}")
            return False
        
        share_key = f"{credential_name}:{target_agent}"
        self._sharing_policies[share_key] = {
            "permissions": permissions,
            "shared_at": datetime.now().isoformat(),
            "shared_by": agent_id
        }
        
        self._log_action("SHARE", credential_name, agent_id, 
                        {"target_agent": target_agent, "permissions": permissions})
        print(f"🤝 Shared '{credential_name}' with agent '{target_agent}'")
        print(f"   Permissions: {', '.join(permissions)}")
        return True
    
    def receive_shared_credential(self, credential_name: str, 
                                  receiving_agent: str) -> Optional[Credential]:
        """Receive a credential that was shared with this agent."""
        share_key = f"{credential_name}:{receiving_agent}"
        
        if share_key not in self._sharing_policies:
            self._log_action("RECEIVE_DENIED", credential_name, receiving_agent,
                           {"reason": "no_share_policy"})
            print(f"🚫 Access denied - '{credential_name}' not shared with '{receiving_agent}'")
            return None
        
        credential = self._credentials.get(credential_name)
        if credential:
            self._log_action("RECEIVE", credential_name, receiving_agent)
            print(f"📥 Received shared credential: {credential_name}")
            return credential
        return None
    
    def get_audit_logs(self, limit: int = 50) -> List[AuditLogEntry]:
        """Get recent audit log entries."""
        return self._audit_logs[-limit:]
    
    def print_audit_report(self) -> None:
        """Print a formatted audit report."""
        print("\n" + "=" * 60)
        print("AUDIT LOG REPORT")
        print("=" * 60)
        print(f"Vault: {self.vault_name}")
        print(f"Total Events: {len(self._audit_logs)}")
        print("-" * 60)
        
        for entry in self._audit_logs:
            print(f"[{entry.timestamp}] {entry.action:20} | "
                  f"Agent: {entry.agent_id:15} | Credential: {entry.credential_name or 'N/A'}")
        print("=" * 60)


# =============================================================================
# Example Usage
# =============================================================================

def main():
    """Main demonstration of AgentVault functionality."""
    
    print("\n" + "=" * 60)
    print("AGENTVAULT: SECURE CREDENTIAL MANAGEMENT DEMO")
    print("=" * 60 + "\n")
    
    # -------------------------------------------------------------------------
    # Step 1: Create a Secure Vault
    # -------------------------------------------------------------------------
    print("STEP 1: Creating Secure Vault")
    print("-" * 60)
    
    # In production, use a strong, randomly generated key
    # NEVER hardcode keys in production code
    encryption_key = os.environ.get("AGENTVAULT_KEY", "demo-key-32-chars-long-1234567890")
    
    vault = Vault(
        encryption_key=encryption_key,
        vault_name="production-vault"
    )
    vault.initialize()
    print()
    
    # -------------------------------------------------------------------------
    # Step 2: Add Credentials
    # -------------------------------------------------------------------------
    print("STEP 2: Adding Credentials")
    print("-" * 60)
    
    # API Key for OpenAI
    openai_credential = Credential(
        name="openai-api-key",
        value="sk-demo-openai-key-12345",
        metadata={
            "service": "openai",
            "environment": "production",
            "rotation_date": (datetime.now() + timedelta(days=90)).isoformat()
        }
    )
    vault.store_credential(openai_credential)
    
    # Database password
    db_credential = Credential(
        name="database-password",
        value="SuperSecureDBPassword123!",
        metadata={
            "service": "postgresql",
            "host": "db.production.internal",
            "database": "app_database"
        }
    )
    vault.store_credential(db_credential)
    
    # External service token
    slack_token = Credential(
        name="slack-bot-token",
        value="xoxb-demo-slack-token-67890",
        metadata={
            "service": "slack",
            "workspace": "my-team",
            "scopes": ["chat:write", "users:read"]
        }
    )
    vault.store_credential(slack_token)
    print()
    
    # -------------------------------------------------------------------------
    # Step 3: List Available Credentials
    # -------------------------------------------------------------------------
    print("STEP 3: Listing Vault Contents")
    print("-" * 60)
    credentials = vault.list_credentials()
    print(f"Stored credentials ({len(credentials)}):")
    for cred_name in credentials:
        print(f"  - {cred_name}")
    print()
    
    # -------------------------------------------------------------------------
    # Step 4: Retrieve a Credential
    # -------------------------------------------------------------------------
    print("STEP 4: Retrieving Credentials")
    print("-" * 60)
    
    # Retrieve OpenAI key
    cred = vault.get_credential("openai-api-key")
    if cred:
        print(f"  Value: {cred.value[:10]}... (truncated)")
        print(f"  Metadata: {json.dumps(cred.metadata, indent=4)}")
    print()
    
    # -------------------------------------------------------------------------
    # Step 5: Share Credentials Between Agents
    # -------------------------------------------------------------------------
    print("STEP 5: Sharing Credentials Between Agents")
    print("-" * 60)
    
    # Share OpenAI key with agent-123
    vault.share_credential(
        credential_name="openai-api-key",
        target_agent="agent-123",
        permissions=["read"]
    )
    
    # Share Slack token with agent-456
    vault.share_credential(
        credential_name="slack-bot-token",
        target_agent="agent-456",
        permissions=["read", "write"]
    )
    print()
    
    # -------------------------------------------------------------------------
    # Step 6: Receiving Shared Credentials
    # -------------------------------------------------------------------------
    print("STEP 6: Receiving Shared Credentials")
    print("-" * 60)
    
    # Agent-123 receives the shared credential
    received = vault.receive_shared_credential("openai-api-key", "agent-123")
    if received:
        print(f"  Agent-123 received: {received.name}")
    
    # Try to access without permission (should fail)
    denied = vault.receive_shared_credential("database-password", "agent-123")
    if not denied:
        print("  (Expected) Agent-123 cannot access database-password (not shared)")
    
    # Agent-456 receives Slack token
    received2 = vault.receive_shared_credential("slack-bot-token", "agent-456")
    if received2:
        print(f"  Agent-456 received: {received2.name}")
    print()
    
    # -------------------------------------------------------------------------
    # Step 7: Audit Logging
    # -------------------------------------------------------------------------
    print("STEP 7: Audit Logging")
    print("-" * 60)
    
    vault.print_audit_report()
    print()
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("""
Summary:
- Created encrypted vault with AES-256-GCM simulation
- Stored 3 credentials with metadata
- Listed all stored credentials
- Retrieved credentials with access logging
- Shared credentials between agents with granular permissions
- Demonstrated access control (denied unauthorized access)
- Generated comprehensive audit trail

In Production:
- Use actual AES-256-GCM encryption
- Store encryption keys in HSM or KMS (AWS KMS, Azure Key Vault, etc.)
- Enable automatic credential rotation
- Implement network access controls
- Use TLS for all communication
- Regularly review audit logs
    """)


if __name__ == "__main__":
    main()
