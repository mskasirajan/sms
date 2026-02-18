// ─── Auth ────────────────────────────────────────────────────────────────────

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  school_id: number;
  is_active: boolean;
}

export type UserRole =
  | 'super_admin'
  | 'school_admin'
  | 'principal'
  | 'teacher'
  | 'accountant'
  | 'librarian'
  | 'transport_manager'
  | 'student'
  | 'parent';

// ─── School ──────────────────────────────────────────────────────────────────

export interface School {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  logo_url?: string;
}

export interface AcademicYear {
  id: number;
  school_id: number;
  year_label: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
}

// ─── Student ─────────────────────────────────────────────────────────────────

export interface Student {
  id: number;
  school_id: number;
  user_id: number;
  admission_number: string;
  full_name: string;
  date_of_birth: string;
  gender: 'Male' | 'Female' | 'Other';
  address: string;
  phone?: string;
  email?: string;
  class_id?: number;
  section_id?: number;
  class_name?: string;
  section_name?: string;
  is_active: boolean;
  created_at: string;
}

export interface StudentCreate {
  admission_number: string;
  full_name: string;
  date_of_birth: string;
  gender: 'Male' | 'Female' | 'Other';
  address: string;
  phone?: string;
  email?: string;
  class_id?: number;
  section_id?: number;
}

// ─── Teacher ─────────────────────────────────────────────────────────────────

export interface Teacher {
  id: number;
  school_id: number;
  user_id: number;
  employee_id: string;
  full_name: string;
  email: string;
  phone: string;
  qualification: string;
  specialization?: string;
  joining_date: string;
  is_active: boolean;
  created_at: string;
}

export interface TeacherCreate {
  employee_id: string;
  full_name: string;
  email: string;
  phone: string;
  qualification: string;
  specialization?: string;
  joining_date: string;
}

// ─── Attendance ───────────────────────────────────────────────────────────────

export type AttendanceStatus = 'Present' | 'Absent' | 'Late' | 'Half-Day';

export interface AttendanceSession {
  id: number;
  school_id: number;
  class_id: number;
  section_id?: number;
  teacher_id: number;
  session_date: string;
  academic_year_id: number;
}

export interface StudentAttendance {
  id: number;
  session_id: number;
  student_id: number;
  student_name: string;
  admission_number: string;
  status: AttendanceStatus;
  remarks?: string;
}

export interface AttendanceMarkRequest {
  class_id: number;
  section_id?: number;
  session_date: string;
  records: { student_id: number; status: AttendanceStatus; remarks?: string }[];
}

export interface AttendanceReport {
  student_id: number;
  student_name: string;
  admission_number: string;
  total_days: number;
  present: number;
  absent: number;
  late: number;
  percentage: number;
}

// ─── Fees ─────────────────────────────────────────────────────────────────────

export interface FeeStructure {
  id: number;
  school_id: number;
  academic_year_id: number;
  class_id: number;
  name: string;
  amount: number;
  due_date: string;
}

export interface Invoice {
  id: number;
  school_id: number;
  student_id: number;
  student_name: string;
  admission_number: string;
  academic_year_id: number;
  total_amount: number;
  paid_amount: number;
  due_amount: number;
  status: 'Pending' | 'Partial' | 'Paid' | 'Overdue';
  due_date: string;
  created_at: string;
}

export interface Payment {
  id: number;
  invoice_id: number;
  student_id: number;
  amount: number;
  payment_method: 'Cash' | 'UPI' | 'Card' | 'Bank Transfer';
  transaction_id?: string;
  paid_at: string;
}

export interface PaymentCreate {
  invoice_id: number;
  amount: number;
  payment_method: 'Cash' | 'UPI' | 'Card' | 'Bank Transfer';
  transaction_id?: string;
}

// ─── Exams ────────────────────────────────────────────────────────────────────

export interface Exam {
  id: number;
  school_id: number;
  academic_year_id: number;
  name: string;
  exam_type: 'Unit Test' | 'Mid Term' | 'Final' | 'Monthly';
  start_date: string;
  end_date: string;
  is_active: boolean;
}

export interface ExamSchedule {
  id: number;
  exam_id: number;
  class_id: number;
  subject_id: number;
  subject_name: string;
  exam_date: string;
  start_time: string;
  end_time: string;
  max_marks: number;
  pass_marks: number;
}

export interface Mark {
  id: number;
  exam_schedule_id: number;
  student_id: number;
  student_name: string;
  admission_number: string;
  marks_obtained: number;
  max_marks: number;
  grade: string;
  is_pass: boolean;
  remarks?: string;
}

export interface MarksUpload {
  exam_schedule_id: number;
  records: { student_id: number; marks_obtained: number; remarks?: string }[];
}

// ─── Class / Section ──────────────────────────────────────────────────────────

export interface Class {
  id: number;
  school_id: number;
  name: string;
  numeric_level: number;
}

export interface Section {
  id: number;
  class_id: number;
  name: string;
}

// ─── Pagination ───────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ApiError {
  detail: string;
}
