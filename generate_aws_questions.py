import csv
import random
import uuid

# Domain weights and question counts
domains = {
    "Domain 1: Design Secure Architectures": {"weight": 0.30, "count": 600},
    "Domain 2: Design Resilient Architectures": {"weight": 0.26, "count": 520},
    "Domain 3: Design High-Performing Architectures": {"weight": 0.24, "count": 480},
    "Domain 4: Design Cost-Optimized Architectures": {"weight": 0.20, "count": 400}
}

# Service and scenario templates for each domain
question_templates = {
    "Domain 1: Design Secure Architectures": [
        {
            "service": "Amazon Cognito",
            "question": "A company needs to manage user authentication for a web application. Which AWS service should the solutions architect recommend?",
            "correct_answer": "Amazon Cognito",
            "explanation": "Amazon Cognito provides user authentication, authorization, and user management for web and mobile applications.",
            "incorrect_answers": [
                {"option": "AWS IAM", "reason": "IAM manages AWS resource access, not user authentication for applications."},
                {"option": "AWS KMS", "reason": "KMS handles encryption keys, not user authentication."},
                {"option": "AWS Shield", "reason": "Shield protects against DDoS attacks, not authentication."}
            ]
        },
        {
            "service": "AWS KMS",
            "question": "A solutions architect needs to encrypt sensitive data stored in an Amazon S3 bucket. Which service should be used?",
            "correct_answer": "AWS Key Management Service (KMS)",
            "explanation": "AWS KMS provides managed encryption keys for securing data in S3 and other services.",
            "incorrect_answers": [
                {"option": "Amazon Inspector", "reason": "Inspector performs vulnerability assessments, not encryption."},
                {"option": "AWS Secrets Manager", "reason": "Secrets Manager stores secrets, not general data encryption."},
                {"option": "Amazon Macie", "reason": "Macie detects sensitive data, not encrypts it."}
            ]
        },
        {
            "service": "AWS Security Hub",
            "question": "A company wants to aggregate security findings from multiple AWS accounts. Which service should be used?",
            "correct_answer": "AWS Security Hub",
            "explanation": "AWS Security Hub aggregates findings from services like GuardDuty, Inspector, and Macie, and supports cross-account security scores.",
            "incorrect_answers": [
                {"option": "Amazon GuardDuty", "reason": "GuardDuty detects threats but does not aggregate findings across accounts."},
                {"option": "AWS Systems Manager", "reason": "Systems Manager manages resources, not security findings."},
                {"option": "Amazon Macie", "reason": "Macie detects sensitive data but does not aggregate findings."}
            ]
        }
    ],
    "Domain 2: Design Resilient Architectures": [
        {
            "service": "Amazon RDS Multi-AZ",
            "question": "A solutions architect needs to ensure a relational database remains available during an Availability Zone outage. Which configuration should be used?",
            "correct_answer": "Deploy Amazon RDS with Multi-AZ enabled",
            "explanation": "Amazon RDS with Multi-AZ enabled creates a standby replica in another AZ, enabling automatic failover.",
            "incorrect_answers": [
                {"option": "Use DynamoDB with global tables", "reason": "DynamoDB global tables provide multi-region replication, not AZ-level failover for relational databases."},
                {"option": "Configure RDS with read replicas only", "reason": "Read replicas improve read performance but do not support automatic failover."},
                {"option": "Deploy Redshift in a single AZ", "reason": "Redshift in a single AZ lacks high availability."}
            ]
        },
        {
            "service": "Auto Scaling",
            "question": "A company’s EC2-based application needs improved fault tolerance. Which solution should the architect implement?",
            "correct_answer": "Use an Auto Scaling group across multiple Availability Zones",
            "explanation": "Auto Scaling across multiple AZs distributes instances and replaces failed ones, improving fault tolerance.",
            "incorrect_answers": [
                {"option": "Deploy in multiple regions with Route 53", "reason": "Multi-region deployment is complex and not the primary solution for AZ-level fault tolerance."},
                {"option": "Add a second EC2 instance in the same AZ", "reason": "Same-AZ instances do not protect against AZ outages."},
                {"option": "Use S3 for application data", "reason": "S3 is for storage, not compute fault tolerance."}
            ]
        },
        {
            "service": "Elastic Load Balancer",
            "question": "A critical application must distribute traffic across multiple Availability Zones. Which service should be used?",
            "correct_answer": "Elastic Load Balancer",
            "explanation": "Elastic Load Balancer distributes traffic across EC2 instances in multiple AZs, ensuring availability.",
            "incorrect_answers": [
                {"option": "Amazon Route 53", "reason": "Route 53 handles DNS and failover, not intra-region traffic distribution."},
                {"option": "AWS Global Accelerator", "reason": "Global Accelerator improves global performance, not AZ-level distribution."},
                {"option": "Amazon CloudFront", "reason": "CloudFront is a CDN for caching, not load balancing."}
            ]
        }
    ],
    "Domain 3: Design High-Performing Architectures": [
        {
            "service": "Amazon CloudFront",
            "question": "A solutions architect needs to reduce latency for a web application’s global users. Which service should be used?",
            "correct_answer": "Amazon CloudFront",
            "explanation": "Amazon CloudFront is a CDN that caches content at edge locations, reducing latency for global users.",
            "incorrect_answers": [
                {"option": "Amazon S3 Transfer Acceleration", "reason": "S3 Transfer Acceleration speeds up uploads, not content delivery."},
                {"option": "AWS Direct Connect", "reason": "Direct Connect provides dedicated connectivity, not global caching."},
                {"option": "Amazon Route 53", "reason": "Route 53 handles DNS, not content delivery."}
            ]
        },
        {
            "service": "Amazon RDS read replicas",
            "question": "A company’s RDS database has high read latency. Which solution improves read performance?",
            "correct_answer": "Add read replicas to the RDS database",
            "explanation": "RDS read replicas offload read traffic, improving performance for read-heavy workloads.",
            "incorrect_answers": [
                {"option": "Enable Multi-AZ deployment", "reason": "Multi-AZ improves availability, not read performance."},
                {"option": "Use Amazon Redshift", "reason": "Redshift is for data warehousing, not general-purpose databases."},
                {"option": "Increase RDS instance size", "reason": "Increasing instance size is less efficient than read replicas."}
            ]
        }
    ],
    "Domain 4: Design Cost-Optimized Architectures": [
        {
            "service": "S3 Intelligent-Tiering",
            "question": "A company stores infrequently accessed data in S3. How can costs be reduced while maintaining availability?",
            "correct_answer": "Use S3 Intelligent-Tiering",
            "explanation": "S3 Intelligent-Tiering automatically moves infrequently accessed data to lower-cost tiers while maintaining availability.",
            "incorrect_answers": [
                {"option": "Use S3 Standard", "reason": "S3 Standard is for frequent access, not cost-optimized for infrequent data."},
                {"option": "Transition to S3 Glacier", "reason": "S3 Glacier has retrieval delays, reducing availability."},
                {"option": "Enable versioning", "reason": "Versioning increases costs by storing multiple object versions."}
            ]
        },
        {
            "service": "AWS Lambda",
            "question": "A workload with variable demand needs cost optimization. Which approach is most cost-effective?",
            "correct_answer": "Deploy the workload on AWS Lambda",
            "explanation": "AWS Lambda scales automatically and charges only for execution time, ideal for variable demand.",
            "incorrect_answers": [
                {"option": "Use Reserved Instances", "reason": "Reserved Instances are for steady workloads, not variable demand."},
                {"option": "Use Dedicated Hosts", "reason": "Dedicated Hosts are expensive and suited for licensing needs."},
                {"option": "Increase instance sizes", "reason": "Larger instances are costly and inefficient for variable demand."}
            ]
        }
    ]
}

def generate_question(template):
    question_id = str(uuid.uuid4())
    correct_option = random.choice(["A", "B", "C", "D"])
    options = [template["correct_answer"]] + [x["option"] for x in template["incorrect_answers"]]
    random.shuffle(options)
    correct_index = options.index(template["correct_answer"])
    options_map = {0: "A", 1: "B", 2: "C", 3: "D"}
    correct_letter = options_map[correct_index]
    
    # Generate Options
    options_html = "".join(f"<li>{options_map[i]}. {opt}</li>" for i, opt in enumerate(options))
    
    # Generate OptionsWithCorrect
    options_with_correct = "".join(
        f"<li{' class=\"correct\"' if i == correct_index else ''}>{options_map[i]}. {opt}</li>"
        for i, opt in enumerate(options)
    )
    
    # Generate CorrectOptions
    incorrect_explanations = [
        f"<li><strong>{options_map[i]}:</strong>&nbsp;{template['incorrect_answers'][j]['reason']}</li>"
        for j, (i, opt) in enumerate(enumerate(options))
        if opt != template["correct_answer"]
    ]
    correct_options = (
        f"<div>{correct_letter}</div>"
        f"<strong>Explanation:</strong> {template['explanation']}<br>"
        f"<strong>Incorrect answers:</strong><ul>{''.join(incorrect_explanations)}</ul>"
    )
    
    return [
        template["question"],
        options_html,
        options_with_correct,
        correct_options
    ]

# Generate questions
questions = []
for domain, info in domains.items():
    templates = question_templates[domain]
    for _ in range(info["count"]):
        template = random.choice(templates)
        questions.append(generate_question(template))

# Write to CSV
with open("aws_saa_questions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["Question", "Options", "OptionsWithCorrect", "CorrectOptions"])
    writer.writerows(questions)