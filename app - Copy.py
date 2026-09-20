import os
import pandas as pd
import streamlit as st
class AppointmentManager:
 def __init__(self,filename="appointments_data.csv"):
    self.filename=filename
    self.data=self.load_data()

def load_data(self):
    if os.path.exists(self.filename):
       return pd.read_csv(self.name) 
    else:
        df=pd.DataFrame(["appt_id","patient_name","phone_number","department","appt_Date","state"])
        df.to_csv(self.filename,index=False)
        return df
def save_data(self):
    self.data.to_csv(self.filename,index=False)    
def add_appointment(self,name,phone,department,appt_date,state):
  df=self.data
  new_id=int(df["new_id"].max())+1 if not df.empty else 101
  new_row={new_id:"appt_id",name:"patient_name",phone:"phone_number",department:"department",str(appt_date):"appt_date",state:"confirmed"} 
  self.data=pd.concat([df,pd.DataFrame([new_row])],index=False)
  self.save_data()
  return new_id
def update_status(self,appt_id,new_status):
    self.data.loc[self.data["appt_id"]==appt_date,"state"]=new_status
    self.save_data()
st.set_page_config(page_title="Smart Appointment System",page_icon="📆",layout="wide")
if "manager" not in st.seesion_state:
   st.session_state.manager=AppointmentManager()
manager=st.session_state.manger
st.title("Smart Appiontment & Tracking system")
st.markdown("----")
menu=st.sidebar.selecbox("main menu",["Book a New Appointment","Appointment Tracking and control panel","Dashboard & Data Analysis" ])
if menu =="Book a New Appointment":
    st.header ("📝 Register New Appointment Reservation")
    with st.form("booking_form"):
        col1,col2=st.columns(2)
        with col1:
            patient_name=st.text_input("patient`s triple name :")
            phone=st.text_input("phone number :")
        with col2:
            department=st.selectbox("department required",["internalization","teeth","children","bones","orthopedic"])
            appt_date=st.date_input("Date of appointement:")
            sumbit_button =st.form_sumbit_button(label="confirmation of reservation",use_container_width=True)
    if sumbit_button:
        if patient_name and phone:
            new_id=manager.add_appointment(patient_name,phone,department,appt_date)   
            st.success (f"Appointment booked sucessfully! your reservation_num is:{new_id}")
        else:
            st.error("please,Entre at least patient_name and phone_number") 
elif menu =="Appointment tracking and control panel":
    st.header("Appointment Management and Dashboard")
    df=manager.data
    
    col1,col2,col3=st.columns(3)
    total_booking =len(df)
    confirmed_count=len(df[df["state"]=="confirmed"])
    pending_count=len(df[df["state"]=="waiting"])
    col1.metric("total_booking",total_booking,delta="total_patient")
    col2.metric("confirmed_Appointments",confirmed_count)
    col3.metric("waiting_list",pending_count)
    st.markdown("-------")
    search_query=st.text_input("Search by name or phone_number")
    selected_status=st.selectbox(["All","waiting","confirmed","canceled"],"Filter according to status")
    filtered_df=df.copy()
    if search_query:
      filtered_df=filtered_df[filtered_df["patient_name"].str.contains(search_query,na=False)|filtered_df["phone_number"].str.contains(search_query,na=False)]
    if selected_status !="All":
           filtered_df=filtered_df[filtered_df["state"]==selected_status]
    st.dataframe(filtered_df,use_container_width=True)
    st.markdown("-----") 
    st.subheader("update status")
    if not df.empty:
                  selected_id=st.selectbox("choice appt_id for update",df["appt_id"].tolist() )
                  new_status=st.selectbox("new_state",["confirmed","waiting","canceled"])
    if st.button("update_state"):
           manager.update_status(selected_id,new_status)
           st.success(f"successfully update status {selected_id}")
           st.rerun()     
elif menu=="Dashboard & Data Analysis":
    st.header("Analytics Dashboard")
    df=manager.data
    if df.empty:
        st.warning("There is not enough data for the deshboard presentation at this time .Add reservations first")
    else:
        col1,col2,col3,col4=st.columns(4)
        total_booking=len(df)
        confirmed_count=len(df[df["state"]=="confirmed"])
        pending_count=len(df[df["state"]=="waiting"])
        canceled_count=len(df[df["state"]=="canceled"])
        col1.metric("total_booking",total_booking,delta="total_patient")
        col2.metric("confirmed_Appointments",confirmed_count)
        col3.metric("waiting_list",pending_count)            
        col4.metric("cancel_list",canceled_count)
        st.markdown("-----")
        col_chart1,col_chart2=st.columns(2)
        with col_chart1:
          st.subheader("Distribution by Department")
          dept_counts=df["department"].value_counts()
          st.bar_char(dept_counts)
        with col_chart2:
            st.subheader("General Booking Status")
            status_count=df["state"]
            st.bar_char(status_count)
        st.markdown("----")
        st.subheader("Clinics pressure and  booking capacity status")
        max_capacity_per_dept=10
        for dept in dept_counts.index:
            current_dept_booking=dept_counts
            available_slots=max_capacity_per_dept-current_dept_booking
            progress_val=min(current_dept_booking/max_capacity_per_dept,1.0)
            st.text(f"department({dept}):current_booking({current_dept_booking})from({max_capacity_per_dept})")
            st.progress(progress_val)
            if available_slots > 0:
                st.caption(f"more slots available in this {available_slots}department")
            else:
                st.warning("sorry,the department is completely full.No seats available currently")

                               