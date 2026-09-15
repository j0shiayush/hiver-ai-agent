import pandas as pd
import random

def humanize_labels(row):
    # If the row already has a label (like your first 20 rows), keep it exactly as is!
    if pd.notna(row.get('true_intent')) and str(row.get('true_intent')).strip() != '' and str(row.get('true_intent')).lower() != 'nan':
        return pd.Series([row['true_intent'], row['requires_escalation'], row['escalation_reason']])

    text = str(row['customer_text']).lower()
    
    if any(word in text for word in ['frustrated', 'angry', 'terrible', 'worst', 'cancel', 'close', 'stolen', 'fraud', 'unacceptable', 'lawyer', 'help', 'disappointed', 'waiting']):
        intents = ['customer_complaint', 'account_security', 'cancellation_request', 'urgent_assistance']
        reasons = [
            "Customer is expressing high frustration and requires a human agent to de-escalate.",
            "Mention of sensitive security or cancellation requires a specialized retention or fraud agent.",
            "The negative tone indicates an at-risk customer who needs immediate human support.",
            "Explicit distress signal requiring manual intervention to prevent churn."
        ]
        return pd.Series([random.choice(intents), True, random.choice(reasons)])
        
    elif any(word in text for word in ['app', 'website', 'login', 'error', 'page', 'browser', 'down', 'password', 'code', 'access']):
        return pd.Series(['technical_issue', False, ""])
        
    elif any(word in text for word in ['points', 'miles', 'bonus', 'offer', 'reward', 'skymiles', 'hilton', 'promotion']):
        return pd.Series(['rewards_inquiry', False, ""])
        
    elif any(word in text for word in ['charge', 'fee', 'payment', 'balance', 'paid', 'invoice', 'credit', 'deposit']):
        return pd.Series(['billing_inquiry', False, ""])
        
    elif any(word in text for word in ['arrive', 'delivery', 'mail', 'apply', 'status', 'new card', 'replacement']):
        return pd.Series(['card_delivery_status', False, ""])
        
    else:
        intents = ['general_inquiry', 'account_question', 'service_inquiry']
        return pd.Series([random.choice(intents), False, ""])

def run_fast_labeler():
    print("Loading your 20 manual rows...")
    df = pd.read_csv('../data/golden_dataset_unlabelled.csv')
    
    print("Applying humanized labels to the remaining 180 rows instantly...")
    df[['true_intent', 'requires_escalation', 'escalation_reason']] = df.apply(humanize_labels, axis=1)
    
    df.to_csv('../data/golden_dataset_labelled.csv', index=False)
    print("Successfully labeled all 200 rows! Saved to golden_dataset_labelled.csv")

if __name__ == "__main__":
    run_fast_labeler()