
lines = []
with open('zaker_postman_collection.json', 'r') as f:
    lines = f.readlines()

# Line 413 is index 412
# Check if it has the comma
if '},' in lines[412]:
    lines[412] = lines[412].replace('},', '}')
    print("Fixed trailing comma at line 413")
else:
    print(f"Line 413 content: {lines[412]}")  
    # Fallback search near the end of "item" list
    for i in range(400, 420):
        if '},' in lines[i] and ']' in lines[i+1]:
             print(f"Found trailing comma at {i+1}: {lines[i]}")
             lines[i] = lines[i].replace('},', '}')
             break

with open('zaker_postman_collection.json', 'w') as f:
    f.writelines(lines)
