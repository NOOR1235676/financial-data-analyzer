#!/usr/bin/env python3
"""
Phase 3: Data Reconciliation
Automatically match transactions between bank and ledger entries
"""

from typing import List, Dict, Tuple
from phase2_parser import ParsedTransaction, AdvancedTransactionParser
from datetime import timedelta

class DataReconciler:
    def __init__(self):
        self.parser = AdvancedTransactionParser()

    def reconcile_transactions(self, bank_transactions: List[ParsedTransaction], ledger_transactions: List[ParsedTransaction],
                               date_tolerance: int = 3, amount_tolerance: float = 0.01) -> List[Tuple[ParsedTransaction, ParsedTransaction, float]]:
        """
        Reconcile transactions between bank statements and customer ledger entries.

        Args:
            bank_transactions (List[ParsedTransaction]): List of bank transactions
            ledger_transactions (List[ParsedTransaction]): List of ledger transactions
            date_tolerance (int): Days difference allowed
            amount_tolerance (float): Amount difference allowed

        Returns:
            List[Tuple[ParsedTransaction, ParsedTransaction, float]]: Matching transactions with scores
        """
        matches = []

        for bank_trans in bank_transactions:
            best_match = None
            best_score = 0

            for ledger_trans in ledger_transactions:
                # Check date proximity
                if abs((bank_trans.date - ledger_trans.date).days) <= date_tolerance:
                    # Check amount similarity
                    if abs(bank_trans.amount - ledger_trans.amount) <= amount_tolerance:
                        # Use description similarity
                        desc_score = self.description_similarity(bank_trans.description, ledger_trans.description)

                        # Combined score
                        score = desc_score - (abs((bank_trans.date - ledger_trans.date).days) * 10) - (abs(bank_trans.amount - ledger_trans.amount) * 100)

                        if score > best_score:
                            best_score = score
                            best_match = ledger_trans

            if best_match:
                matches.append((bank_trans, best_match, best_score))

        return matches

    def description_similarity(self, desc1: str, desc2: str) -> float:
        """Calculate a simplistic similarity score between two descriptions"""
        set1 = set(desc1.lower().split())
        set2 = set(desc2.lower().split())
        common_words = set1.intersection(set2)
        return len(common_words) / max(len(set1), len(set2), 1) * 100

