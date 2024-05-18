import subprocess

# Define the command and arguments
command = [
    'python', 'src/main.py',
    '--br-path', 'D:\Research\Coding\Replication_Package\TransLocator\data\\test_fixed_all_TIMED.json',
    '--kw-model-dir', 'F:\Models\masked_bugreport_full',
    '--ce-model-dir', 'F:\Models\Cross_encoder\CodeBert_Full_DS_Timed',
    '--L', '10',
    '--topK_rerank', '100',
    '--topN', '10'
]

# Run the command
result = subprocess.run(command, capture_output=True, text=True)

# Print the output and error (if any)
print("Output:\n", result.stdout)
print("Error:\n", result.stderr)
