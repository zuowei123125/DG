import sqlite3
conn = sqlite3.connect('designercep.db')

# Update plugin_groups table - column is current_version_file not version
conn.execute("UPDATE plugin_groups SET current_version_file = 'core-v1.3.1.zip' WHERE id=1")
conn.commit()
print('Updated Default group to core-v1.0.5.zip')

cursor = conn.execute('SELECT * FROM plugin_groups')
print(list(cursor))
conn.close()
