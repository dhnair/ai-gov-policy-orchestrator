import pandas as pd, json

df = pd.read_excel('data/processed/search_results_processed_concepts_v3.xlsx')

allc = []
for x in df['concepts'].dropna():
    for c in str(x).split(','):
        allc.append(c.strip())

cnt = pd.Series(allc).value_counts().head(30)

out = {
    'top_keywords': cnt.index.tolist(),
    'top_counts': cnt.tolist()
}

with open('app/assets/keyword_stats.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("keyword_stats.json generated successfully!")
