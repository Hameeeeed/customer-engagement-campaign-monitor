# Customer Engagement Campaign Monitoring System

## Project Overview
A Python-based application that simulates customer engagement campaign delivery across Email, SMS, and Push channels.

## Technologies Used
- Python
- Flask
- SQLite
- SQL
- Requests
- Python Logging

## Features
- Retrieve campaign records through REST APIs
- Track delivered and failed campaigns
- Identify campaign failure reasons
- Generate campaign summary reports
- Generate channel-wise performance reports
- Validate campaign IDs
- Handle missing campaign records
- Record application and campaign failure logs

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | API health check |
| GET | /campaigns | Retrieve all campaigns |
| GET | /campaigns/<campaign_id> | Retrieve one campaign |
| GET | /campaigns/failed | Retrieve failed campaigns |
| GET | /reports/summary | Overall campaign summary |
| GET | /reports/channel | Channel-wise report |

## Sample Results
- Total campaigns: 8
- Delivered: 4
- Failed: 4
- Success rate: 50%

## Channel Performance
| Channel | Total | Delivered | Failed |
|---|---:|---:|---:|
| Email | 3 | 2 | 1 |
| Push | 3 | 1 | 2 |
| SMS | 2 | 1 | 1 |

## Error Handling
- HTTP 200: Successful request
- HTTP 400: Invalid campaign ID
- HTTP 404: Campaign not found

## Logging
Application startup and campaign delivery failures are recorded in logs/application.log.

## Installation
pip install flask requests

## Execution
Developed and tested using Google Colab. Execute the notebook cells in order to initialize the database and run the Flask API.

## Author
Mohd Hameed Ahmad