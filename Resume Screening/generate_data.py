import pandas as pd
import random

# Expanded categories and corresponding skills for both engineering and non-engineering fields
categories_skills = {
    "Data Scientist": ["Machine Learning", "Data Analysis", "Python", "Statistics", "R", "Deep Learning", "Big Data", "Data Visualization"],
    "Software Engineer": ["Java", "Python", "C++", "JavaScript", "SQL", "HTML/CSS", "Django", "React", "Node.js", "Angular", "RESTful APIs"],
    "Project Manager": ["Project Planning", "Team Leadership", "Communication", "Risk Management", "Agile", "Stakeholder Management", "Scrum", "Budgeting"],
    "Business Analyst": ["Requirements Analysis", "Data Modeling", "Business Process Improvement", "SQL", "Excel", "Tableau", "Business Intelligence"],
    "UX/UI Designer": ["User Research", "Wireframing", "Prototyping", "UI Design", "UX Design", "Adobe XD", "Sketch", "Figma"],
    "Network Engineer": ["Network Protocols", "Routing and Switching", "Firewalls", "Network Security", "TCP/IP", "LAN/WAN", "Cisco", "Juniper", "CCNA"],
    "Mechanical Engineer": ["CAD", "SolidWorks", "Thermodynamics", "Fluid Mechanics", "Product Design", "Manufacturing Processes", "AutoCAD", "ANSYS"],
    "Electrical Engineer": ["Circuit Design", "Electronics", "Microcontrollers", "VHDL", "PCB Design", "Embedded Systems", "Power Systems", "MATLAB"],
    "Civil Engineer": ["Structural Analysis", "AutoCAD", "Project Management", "Construction", "Geotechnical Engineering", "Surveying", "Revit", "STAAD Pro"],
    "Marketing Specialist": ["SEO", "Content Marketing", "Social Media", "Email Marketing", "Google Analytics", "Brand Management", "PPC", "Market Research"],
    "Human Resources Manager": ["Recruitment", "Employee Relations", "HR Policies", "Performance Management", "Talent Acquisition", "Onboarding", "Compensation and Benefits"],
    "Accountant": ["Financial Reporting", "Tax Preparation", "Auditing", "QuickBooks", "Excel", "Budgeting", "Payroll", "Accounts Payable/Receivable"],
    "Chemical Engineer": ["Process Engineering", "Chemical Reactions", "Thermodynamics", "Process Design", "Safety Management", "ChemCAD", "HYSYS"],
    "Data Analyst" : ["Data Analysis", "SQL", "Excel", "Statistics", "Reporting", "Data Visualization", "Python", "R"],
    "Sales Executive" : ["Sales", "Negotiation", "Client Management", "Lead Generation", "Communication", "Marketing", "CRM"],
    "Web Developer" : ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js", "PHP", "WordPress", "Responsive Design"],
    "Application Developer" : ["Java", "Kotlin", "Swift", "Objective-C", "Android Development", "iOS Development", "Mobile App Design", "Firebase", "RESTful APIs"]

}

# Expanded sample phrases for resume experience for both engineering and non-engineering fields
experience_phrases = {
    "Data Scientist": [
        "Experienced in developing machine learning models for predictive analytics.",
        "Proficient in analyzing large datasets to extract meaningful insights.",
        "Skilled in using Python libraries such as Pandas, NumPy, and Scikit-learn."
    ],
    "Software Engineer": [
        "Proficient in developing scalable and efficient software solutions using Java.",
        "Experienced in web development with Python and Django framework.",
        "Skilled in front-end development with React and back-end with Node.js."
    ],
    "Project Manager": [
        "Strong expertise in project planning and execution.",
        "Experienced in leading cross-functional teams to deliver projects on time and within budget.",
        "Skilled in communication and stakeholder management."
    ],
    "Business Analyst": [
        "Experienced in analyzing business processes and identifying improvement opportunities.",
        "Skilled in data modeling and SQL for querying databases.",
        "Proficient in using Tableau for data visualization and reporting."
    ],
    "UX/UI Designer": [
        "Experienced in conducting user research and creating wireframes and prototypes.",
        "Skilled in UI and UX design principles to create intuitive and user-friendly interfaces.",
        "Proficient in using design tools such as Adobe XD, Sketch, and Figma."
    ],
    "Network Engineer": [
        "Skilled in designing and implementing network solutions to meet business requirements.",
        "Experienced in configuring and troubleshooting network devices such as routers and switches.",
        "Proficient in network security protocols and best practices."
    ],
    "Mechanical Engineer": [
        "Experienced in using CAD software for product design and development.",
        "Skilled in thermodynamics and fluid mechanics.",
        "Proficient in manufacturing processes and material science."
    ],
    "Electrical Engineer": [
        "Experienced in circuit design and electronics.",
        "Skilled in working with microcontrollers and embedded systems.",
        "Proficient in PCB design and power systems."
    ],
    "Civil Engineer": [
        "Experienced in structural analysis and project management.",
        "Skilled in using AutoCAD and other design software.",
        "Proficient in geotechnical engineering and construction management."
    ],
    "Marketing Specialist": [
        "Experienced in developing and executing SEO strategies.",
        "Skilled in content marketing and social media management.",
        "Proficient in using Google Analytics and other marketing tools."
    ],
    "Human Resources Manager": [
        "Experienced in recruitment and employee relations.",
        "Skilled in developing and implementing HR policies.",
        "Proficient in performance management and talent acquisition."
    ],
    "Accountant": [
        "Experienced in financial reporting and tax preparation.",
        "Skilled in using QuickBooks and Excel for accounting tasks.",
        "Proficient in budgeting, payroll, and accounts payable/receivable."
    ],
    "Chemical Engineer": [
        "Experienced in process engineering and optimization.",
        "Proficient in chemical reaction engineering and thermodynamics.",
        "Skilled in using ChemCAD and HYSYS for process simulation and design."
    ],
    "Data Analyst" : [
        "Experienced in performing data analysis and generating insights from large datasets.",
        "Proficient in SQL for querying databases and extracting information.",
        "Skilled in data visualization using tools like Tableau and Power BI."
    ],
    "Sales Executive" : [
        "Experienced in sales and client management.",
        "Skilled in lead generation and negotiation.",
        "Proficient in using CRM software for sales tracking."
    ],
    "Web Developer" : [
        "Experienced in developing responsive and interactive web applications.",
        "Proficient in front-end technologies like HTML, CSS, and JavaScript.",
        "Skilled in back-end development using Node.js and PHP."
    ],
    "Application Developer" : [
        "Experienced in developing mobile applications for Android and iOS platforms.",
        "Skilled in Java and Kotlin for Android development and Swift for iOS development.",
        "Proficient in using Firebase for backend services and RESTful APIs for communication."
    ]
}

# Generate more random resumes
resumes = []
for _ in range(5000):  # Generate 1000 resumes
    category = random.choice(list(categories_skills.keys()))
    skills = ", ".join(random.sample(categories_skills[category], random.randint(2, len(categories_skills[category]))))
    experience = random.choice(experience_phrases[category])
    resume = f"{experience} Proficient {category.lower()} with a background in {skills.lower()}."
    resumes.append((resume, category, skills))

# Create DataFrame
df = pd.DataFrame(resumes, columns=["Resume", "Category", "Skills"])

# Save DataFrame to CSV
df.to_csv("data.csv", index=False)

print("Generated 5000 datasets successfully.")
