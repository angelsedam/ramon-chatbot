#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[server]
headless = true
enableCORS = false
port = \$PORT

[theme]
base = 'light'
primaryColor = '#4B8BBE'
backgroundColor = '#ffffff'
secondaryBackgroundColor = '#f0f2f6'
textColor = '#000000'
font = 'sans serif'
" > ~/.streamlit/config.toml
