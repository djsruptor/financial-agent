Since you want to prompt an LLM (or a developer) to implement these sequentially, I have broken these down into **Logical Blocks**. 

You should provide these one at a time to ensure the model maintains focus and doesn't hallucinate complex logic it can't actually execute.

---

### Prompt 1: Phase 2 - Candidate Generation & Deterministic Validation
**Context:** *The current system can reconstruct cash flow and forecast budgets. Now we need the "Decision Engine" that takes those numbers and generates valid payment options.*

```python
# --- TODO: Implement Phase 2 Logic ---

def generate_payment_candidates(forecast, user_preferences):
    """
    Tool for the model to propose potential plans.
    Logic: The model interprets 'user_preferences' (e.g., "Pay as fast as possible") 
    and generates a list of proposed payment objects.
    
    Returns: List[Dict] {type, amount, start_date, duration, total_interest}
    """
    pass

def validate_candidate_feasibility(proposed_plan, forecast):
    """
    CRITICAL DETERMINISTIC CHECK (Code-owned)
    This function MUST NOT be an LLM call. It must check the proposed_plan 
    against the 'forecast' object generated in Phase 1.
    
    Rules:
    1. Monthly payment < Available Cash Flow for that month?
    2. Start date >= Today?
    3. Total duration aligns with available timeline?
    
    Returns: {is_valid: bool, error_message: str}
    """
    pass

def rank_and_select_best(candidates, user_preferences):
    """
    Tool for the model to select the winning candidate based on 
    the ranking of valid candidates.
    
    Returns: Best Candidate Object
    """
    pass
```

---

### Prompt 2: Phase 2 - Final Formatting & CSV Export
**Context:** *Once a plan is selected, we need to formalize the output into the specific schema required by the project requirements.*

```python
# --- TODO: Implement Output Formatting ---

def export_final_output(winning_candidate, user_data):
    """
    Takes the final selection and formats it strictly into the 
    required CSV structure (OUT-01, OUT-03).
    
    Schema:
    - ID (Unique)
    - PaymentType (Full / Partial / Installment)
    - ScheduledAmount
    - ScheduledDate
    - EstimatedInterestSaved
    - ConfidenceScore (LLM assigned)
    
    Returns: String (CSV formatted content)
    """
    pass

# Update the orchestrator (run_request) to recognize a 'finish' 
# action that triggers this export.
```

---

### Prompt 3: Phase 3 - Evaluation Framework & Metrics
**Context:** *We need a way to test the system against 25 public examples and generate a performance report.*

```python
# --- TODO: Implement Evaluation Suite ---

def run_evaluation_suite(test_dataset):
    """
    Loop through every example in 'public_examples.json'.
    1. Initialize Orchestrator with each example's context.
    2. Run until 'finish' or MAX_TURNS is reached.
    3. Record: 
       - Success/Failure 
       - Total Turns taken
       - Token Usage (from the usage dictionary)
       - Final Output vs. Ground Truth
    4. Store results in a temporary list.
    """
    pass

def generate_usage_report(eval_results):
    """
    Calculate and format:
    - Average Turn Count
    - Success Rate (%)
    - Total Token Cost (Estimated)
    - Error Distribution (e.g., "Insufficient Evidence" vs "Feasibility Error")
    
    Output to 'evaluation/usage_report.md'
    """
    pass
```

---

### Prompt 4: Phase 3 - Packaging and Final Submission
**Context:** *Final cleanup to ensure the project meets the submission requirements.*

```python
# --- TODO: Implement Build Script ---

def package_submission():
    """
    1. Run evaluation suite to ensure the report is fresh.
    2. Verify all required files exist:
       - src/ (all python files)
       - prompts/ (all system prompts)
       - evaluation/usage_report.md
    3. Zip the directory into 'code.zip'.
    4. Print success message with paths.
    """
    pass
```

### How to use these prompts:
1.  **Step 1:** Send Prompt 1 and ask the LLM to write the full Python implementation, integrating them into your existing `_dispatch` function.
2.  **Step 2:** Once that's working, send Prompt 2 to handle the final output.
3.  **Step 3:** Send Prompts 3 & 4 together as the "Final Packaging" phase.
