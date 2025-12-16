#!/usr/bin/env python3
"""Script to fix indentation issues in streamlit_frontend.py"""

def fix_indentation():
    with open('/workspace/streamlit_frontend.py', 'r') as f:
        lines = f.readlines()
    
    # Process lines to fix indentation
    # We need to find the problematic section and fix it
    fixed_lines = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Fix line 153: if isinstance should have less indentation
        if line_num == 153:
            # Original: "            if isinstance..." (12 spaces)
            # Should be: "        if isinstance..." (8 spaces)
            stripped = line.lstrip()
            fixed_lines.append("    " * 2 + stripped)  # 2 indent levels = 8 spaces
        # Fix lines 154-258: These should have one less level of indentation
        elif 154 <= line_num <= 258:
            # Count leading spaces and reduce by 4
            leading_spaces = len(line) - len(line.lstrip())
            new_leading_spaces = max(0, leading_spaces - 4)
            fixed_lines.append(" " * new_leading_spaces + line.lstrip())
        # Fix line 259: else should align with if isinstance (8 spaces)
        elif line_num == 259:
            stripped = line.lstrip()
            fixed_lines.append("    " * 2 + stripped)  # 2 indent levels = 8 spaces
        # Fix line 260: st.info should align with else (also 8 spaces)
        elif line_num == 260:
            stripped = line.lstrip()
            fixed_lines.append("    " * 2 + stripped)  # 2 indent levels = 8 spaces
        else:
            fixed_lines.append(line)
    
    # Write the fixed file
    with open('/workspace/streamlit_frontend_fixed.py', 'w') as f:
        f.writelines(fixed_lines)

if __name__ == "__main__":
    fix_indentation()