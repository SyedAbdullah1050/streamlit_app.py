import streamlit as st # This line is commented out because it's already imported below
import io # Used for simulating file save content

# --- 1. Streamlit Page Config (Setup) ---
st.set_page_config(
    page_title="CMS Lite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. Data & Logic ---

# Define the Student class (Your structure)
class Student:
    def __init__(self, roll, name, grade, dept):
        self.rollNumber = roll
        self.name = name
        self.className = grade
        self.department = dept

# Hardcoded data from your C code
STUDENTS_DATA = [
    Student(101, "Muhammad Anas", "XI", "CS"),
    Student(102, "Fatima Ali", "XI", "PreEng"),
    Student(103, "Ayesha Siddiqui", "XI", "PreMed"),
    Student(104, "Bilal Khan", "XI", "Commerce"),
    Student(105, "Ahmed Raza", "XI", "CS"),
    Student(106, "Konain Khan", "XI", "PreEng"),
    Student(107, "Usman Hanif", "XI", "PreMed"),
    Student(108, "Maryam Noor", "XI", "Commerce"),
    Student(109, "Zain Ali", "XI", "PreEng"),
    Student(110, "Hamza Tariq", "XI", "CS"),
    Student(201, "Ali Haider", "XII", "CS"),
    Student(202, "Laiba Naseem", "XII", "PreEng"),
    Student(203, "Zoya Iqbal", "XII", "PreMed"),
    Student(204, "Hammad Aslam", "XII", "Commerce"),
    Student(205, "Noor Fatima", "XII", "CS"),
    Student(206, "Muhammad Amir", "XII", "PreEng"),
    Student(207, "Sana Javed", "XII", "PreMed"),
    Student(208, "Rehan Ahmed", "XII", "Commerce"),
    Student(209, "Amina Rafiq", "XII", "PreEng"),
    Student(210, "Syed Abdullah Husain", "XII", "CS")
]

# Helper Data for Departments (Simplified dictionary)
DEPT_INFO = {
    "PreEng": {
        "courses": "Maths, Physics, Chemistry",
        "faculty": ["Maths - Prof. Ovais Khan", "Physics - Prof. Ashfaq", "Chemistry - Dr. Naveed"]
    },
    "PreMed": {
        "courses": "Biology, Physics, Chemistry",
        "faculty": ["Biology - Dr. Ashraf", "Physics - Prof. Rahim", "Chemistry - Prof. Samar Abbas"]
    },
    "CS": {
        "courses": "Maths, Computer Science, Physics",
        "faculty": ["Comp Sci - Prof. Nabiha Faisal", "Physics - Prof. Younus", "Maths - Prof. Adnan"]
    },
    "Commerce": {
        "courses": "Accounting, Business Maths, Statistics",
        "faculty": ["Accounting - Prof. Tehseen", "Statistics - Prof. Ali", "Business Maths - Prof. Saad"]
    }
}

# --- 3. The UI Layout ---

# Sidebar for Navigation
with st.sidebar:
    st.title("🎓 CMS Menu (Lite)")
    page = st.radio("Go to", ["Dashboard", "Student Directory", "Find Student"])
    st.markdown("---")
    st.info("System Status: **Online** 🟢")

# --- Page 1: Dashboard (Simple Metrics) ---
if page == "Dashboard":
    st.title("📊 College Dashboard")
    st.markdown("---")
    
    total_students = len(STUDENTS_DATA) # This line is correct
    dept_counts = {}
    for student in STUDENTS_DATA:
        dept_counts[student.department] = dept_counts.get(student.department, 0) + 1

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", total_students)
    c2.metric("Computer Sci", dept_counts.get('CS', 0))
    c3.metric("Pre-Medical", dept_counts.get('PreMed', 0))
    c4.metric("Commerce", dept_counts.get('Commerce', 0))

    st.markdown("### 📝 System Summary")
    st.write("This application provides quick access to 20 student records and faculty assignments.")


# --- Page 2: Student Directory (Uses standard lists and Markdown) ---
elif page == "Student Directory":
    st.title("👥 Student Directory")
    st.markdown("---")
    
    # Simple list display (Replaces st.dataframe)
    st.markdown("### Student List")
    
    # Create the header row using Markdown
    header = f"| {'Roll No':<8} | {'Name':<25} | {'Class':<5} | {'Department':<15} |"
    st.markdown(header)
    st.markdown("---|---------------------------|-------|------------------|")

    # Generate the table content
    for s in STUDENTS_DATA:
        row = f"| {s.rollNumber:<8} | {s.name:<25} | {s.className:<5} | {s.department:<15} |"
        st.markdown(row)

    # Replaces 'saveStudentsToFile' with a functional download button
    all_data_text = "Roll No | Name | Class | Department\n"
    for s in STUDENTS_DATA:
        all_data_text += f"{s.rollNumber} | {s.name} | {s.className} | {s.department}\n"
    
    st.markdown("---")
    st.download_button(
        label="📥 Download Full List (TXT)",
        data=all_data_text,
        file_name='student_list_lite.txt',
        mime='text/plain',
    )


# --- Page 3: Find Student (No change needed, it was already clean) ---
elif page == "Find Student":
    st.title("🔍 Find Student Details")
    st.markdown("---")
    
    search_roll = st.number_input("Enter Roll Number", min_value=0, step=1)
    
    if search_roll > 0:
        student = next((s for s in STUDENTS_DATA if s.rollNumber == search_roll), None)
        
        if student:
            st.success(f"Record Found: {student.name}")
            dept_data = DEPT_INFO.get(student.department, {"courses": "N/A", "faculty": []})
            
            # Layout with Tabs
            tab1, tab2 = st.tabs(["👤 Profile", "📚 Academic Info"])
            
            with tab1:
                c1, c2 = st.columns(2)
                c1.markdown(f"**Roll No:** {student.rollNumber}")
                c1.markdown(f"**Name:** {student.name}")
                c2.markdown(f"**Class:** {student.className}")
                c2.markdown(f"**Department:** {student.department}")
                
                # Download button for the single record
                report_text = f"Student Record\nName: {student.name}\nRoll: {student.rollNumber}\nDept: {student.department}"
                st.download_button(
                    label="💾 Save this Record",
                    data=report_text,
                    file_name=f"student_{student.rollNumber}.txt",
                    mime="text/plain"
                )

            with tab2:
                st.info(f"**Courses:** {dept_data['courses']}")
                st.write("**Faculty Members:**")
                for teacher in dept_data['faculty']:
                    st.text(f"• {teacher}")
                    
        else:
            st.error("Student not found with that Roll Number.")
