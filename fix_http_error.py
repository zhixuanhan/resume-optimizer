# -*- coding: utf-8 -*-
import re
import urllib.error

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the timeout error return and replace with timeout + HTTPError handling
# Using regex to handle variable whitespace
old_pattern = r"return '\['AI生成失败: The read operation timed out\]'[\s\n]*        except Exception as e:[\s\n]*            return f'\['AI生成失败: \{str\(e\)\}\]'"
new_block = """return '[AI生成失败: The read operation timed out]'
        except urllib.error.HTTPError as e:
            return f'[AI生成失败: HTTP错误 {e.code}]'
        except Exception as e:
            return f'[AI生成失败: {str(e)}]'"""

# Simpler approach - just replace based on the unique timeout error message
search_text = "return '[AI生成失败: The read operation timed out]'"
replace_with = """return '[AI生成失败: The read operation timed out]'
        except urllib.error.HTTPError as e:
            return f'[AI生成失败: HTTP错误 {e.code}]'
        except Exception as e:
            return f'[AI生成失败: {{str(e)}}]'"""

if search_text in content:
    # Find how many blank lines between the timeout return and except
    idx = content.find(search_text)
    # Check next 500 chars
    next_chunk = content[idx:idx+500]
    print(f"Found search text at position {idx}")
    print(f"Next 500 chars: {repr(next_chunk[:200])}")
    
    # Try direct replacement
    content = content.replace(search_text, "return '[AI生成失败: The read operation timed out]'\n        except urllib.error.HTTPError as e:\n            return f'[AI生成失败: HTTP错误 {e.code}]'\n        except Exception as e:\n            return f'[AI生成失败: {str(e)}]'", 1)  # Only replace first occurrence
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: Added HTTPError handling')
else:
    print('ERROR: Search text not found')
    # Show what we find that contains AI生成失败
    for i, line in enumerate(content.split('\n')):
        if 'timed out' in line:
            print(f"Line {i}: {line[:100]}")