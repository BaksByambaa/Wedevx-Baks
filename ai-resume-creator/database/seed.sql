-- Sample Company Data
INSERT INTO companies (name, description, industry, website, size, location) VALUES
('Tech Corp', 'Leading technology company', 'Technology', 'www.techcorp.com', 'ENTERPRISE', 'San Francisco, CA'),
('Startup Inc', 'Innovative startup', 'Software', 'www.startupinc.com', 'STARTUP', 'New York, NY');

-- Sample Job Postings
INSERT INTO job_postings (company_id, title, description, job_type, experience_level) VALUES
((SELECT id FROM companies WHERE name = 'Tech Corp'), 
'Senior Software Engineer', 
'Looking for an experienced software engineer', 
'FULL_TIME', 
'SENIOR'),
((SELECT id FROM companies WHERE name = 'Startup Inc'),
'Junior Developer',
'Great opportunity for new developers',
'FULL_TIME',
'ENTRY');

-- Sample Candidates
INSERT INTO candidates (user_id, personal_info, professional_summary) VALUES
(uuid_generate_v4(),
'{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}',
'Experienced software developer with 5 years of experience'),
(uuid_generate_v4(),
'{"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"}',
'Recent graduate with strong programming skills'); 