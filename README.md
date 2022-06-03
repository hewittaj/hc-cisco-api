# hc-cisco-api
This is an API to retrieve all spam messages for each user in the company.

## Necessary Installs
`pip install email`
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
`pip install requests`
`pip install yagmail`

## Notes
- You will need to rename the .json-example to info.json and fill in your company's information to get this working properly.

## Resources Used
### Cisco Documentation
- <a href="https://www.cisco.com/c/en/us/td/docs/security/esa/esa14-0/api/b_ESA_API_Guide_14-0/b_ESA_API_Guide_chapter_01.html#con_1092445">Cisco Doc</a>
### Tutorial
- <a href="https://github.com/TheAlanNix/SMA-Example-Script/blob/master/sma_example.py">SMA Example</a>
- <a href="https://github.com/gve-sw/esa/blob/master/wrapper-api/Wrapper_API.py">Wrapper API</a>
- <a href="https://www.dataquest.io/blog/last-fm-api-python/">Intermediate Tutorial</a>

### Troubleshooting
- <a href="https://stackoverflow.com/questions/65701773/base64-error-in-encoding-bytes-like-object-is-required-not-str">Encoding Bytes Issue</a>
