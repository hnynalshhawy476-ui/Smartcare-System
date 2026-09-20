import os
import pandas as pd
import streamlit as st
class AppointmentManager:
   csv_columns=["appt_id","patient_name","phone_number","department","appt_Date","state"] 
   



   def __init__(self,filename="appointments_data.csv"):
        self.filename=filename
        self.data=self.load_data()

   def load_data(self):
        if os.path.exists(self.filename):
          try:
             df= pd.read_csv(self.filename)
             for col in self.csv_columns:
              if col not in df.columns:
                  df[col]=""
              if "state" in df.columns:
                df["state"]=df["state"].astype(str).str.lower().str.strip()
                df["appt_id"]=pd.to_numeric(df["appt_id"],errors="coerce")    
       
             return df         
          except Exception as e:
             st.warning(f"reading of file :{e}")
             return pd.DataFrame(columns=self.csv_columns)

           

   
        new_df=pd.DataFrame(columns=self.csv_columns)
        new_df.to_csv(self.filename,index=False)
        return new_df
   def save_data(self):
        self.data.to_csv(self.filename,index=False)    
   def add_appointment(self,name,phone,department,appt_date,state):
        df=self.data
        if df.empty or df["appt_id"].dropna().empty:
            new_id=1
        else: 
            new_id=int(df["appt_id"].max())+1    

            new_row={"appt_id":new_id,"patient_name":name,"phone_number":phone,"department":department,"appt_Date":str(appt_date),"state":state.lower()}

            self.data=pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
            self.save_data()
            return new_id
   def update_status(self,appt_id,new_status):
            self.data.loc[self.data["appt_id"]==appt_id,"state"]=new_status.lower()
            self.save_data()
st.set_page_config(page_title="Smart Appointment System",page_icon="📆",layout="wide")
if "manager" not in st.session_state:
  st.session_state.manager= AppointmentManager()
manager=st.session_state.manager
                
st.sidebar.title("Smart Appiontment & Tracking system")
menu=st.sidebar.selectbox("choose page",["Book a New Appointment(patient)","Appointment Tracking and control panel"," staff Dashboard & Data Analysis" ])
if menu =="Book a New Appointment(patient)":
    st.header ("📝 Register New Appointment Reservation")
    st.markdown("-----")
    with st.form("booking_form"):
        col1,col2=st.columns(2)
        with col1:
            patient_name=st.text_input("patient`s triple name :")
            phone=st.text_input("phone number :")
        with col2:
            department=st.selectbox("department required",["internalization","teeth","children","bones","orthopedic"])
            appt_date=st.date_input("Date of appointement:")
        
        submit_button =st.form_submit_button(label="confirmation of reservation",use_container_width=True)
        if submit_button:
                if patient_name and phone:
                    res_id=manager. add_appointment(patient_name,phone,department,str(appt_date),state="waiting")   
                    st.success (f"Appointment booked sucessfully! your reservation_num is:{res_id}")
                    st.info("status:Waiting for confirmation")
                else:
                    st.error("please,Entre at least patient_name and phone_number") 
elif menu =="Appointment Tracking and control panel":
    st.header("Appointment Management and control panel")
    st.markdown("----")
    try:
        
        df=manager.load_data()
        if df.empty:
            st.warning("No appointments recorded yet.")
        else:
            state_lower=df["state"].str.lower()
            col1,col2,col3=st.columns(3)
            total_booking =len(df)
            confirmed_count=len(df[df["state"]=="confirmed"])
            pending_count=len(df[df["state"].str.lower()=="waiting"])
            col1.metric("total_booking",total_booking,delta="total_patient")
            col2.metric("confirmed_Appointments",confirmed_count)
            col3.metric("waiting_list",pending_count)
            st.markdown("-------")
            st.subheader("Appointments Waiting for Confirmation")
            waiting_df=df[df["state"].str.lower()=="waiting"]
            if waiting_df.empty:
                st.success("No appointments waiting for confirmation.")
            else:
                for _, row in waiting_df.iterrows():
                    c1,c2,c3,c4,c5,c6=st.columns([1,3,2,2,2,2])
                    c1.write(int(row["appt_id"]))
                    c2.write(row["patient_name"])
                    c3.write(str(row["phone_number"]))
                    c4.write(row["department"])
                    c5.write(row["appt_Date"])
                with c6:
                  sub1, sub2=st.columns(2)
                  if sub1.button("☑️",key=f"confirm_{row["appt_id"]}"):              
                    manager.update_status(int(row["appt_id"]),"confirmed")
                    st.rerun()    
                  if sub2.button("❌",key=f"cancel_{row["appt_id"]}"):
                      manager.update_status(int(row["appt_id"]),"cancelled")
                      st.rerun()  
            st.markdown("-------")
            st.subheader("All Appointments")
            search_query=st.text_input("Search by name or phone_number")
            selected_status=st.selectbox("filter according to status ",["ALL","Waiting","confirmed","canceled"])    
            filtered_df=df.copy()
            if search_query:
                filtered_df=filtered_df[filtered_df["patient_name"].astype(str).str.contains(search_query,case=False,na=False)|filtered_df["phone_number"].astype(str).str.contains(search_query,case=False,na=False)]
            if selected_status !="ALL":
                filtered_df=filtered_df[filtered_df["state"]==selected_status.lower()]
            st.dataframe(filtered_df,use_container_width=True)
            st.markdown("-----") 
    except Exception as e:
            st.error(f"wrong:{e}")

elif menu==" staff Dashboard & Data Analysis":
  st.header("Staff Dashboard & Data Analytics")
  st.markdown("----")
  try:
        df=manager.load_data()
        if df.empty:
            st.warning("There is not enough data for the deshboard presentation at this time .Add reservations first")
        else:
            

            col1,col2,col3,col4=st.columns(4)
            total_booking=len(df)
            confirmed_count=len(df[df["state"]=="confirmed"])
            pending_count=len(df[df["state"]=="waiting"])
            canceled_count=len(df[df["state"]=="cancelled"])
            col1.metric("total_booking",total_booking,delta="total_patient")
            col2.metric("confirmed_Appointments",confirmed_count)
            col3.metric("waiting_list",pending_count)            
            col4.metric("cancel_list",canceled_count)
            st.markdown("-----")
            col_chart1,col_chart2=st.columns(2)
            with col_chart1:
                st.subheader("Distribution by Department")
                dept_counts=df["department"].value_counts()
                st.bar_chart(dept_counts)
            with col_chart2:
                st.subheader("General Booking Status")
                status_count=df["state"].value_counts()
                st.bar_chart(status_count)
                st.markdown("----")
            st.subheader("Clinics pressure and  booking capacity status")
            max_capacity_per_dept=10
            dept_counts=df["department"].value_counts()
            for dept,current_dept_booking in dept_counts.items():
                available_slots=max_capacity_per_dept - current_dept_booking
                progress_val=min(current_dept_booking/max_capacity_per_dept,1.0)
                st.text(f"department({dept}):current_booking({current_dept_booking})from({max_capacity_per_dept})")
                st.progress(progress_val)
                if available_slots > 0:
                    st.caption(f"more{available_slots} slots available in this department")
                else:
                    st.warning("sorry,the department is completely full.No seats available currently")

  except Exception as e:

        st.error(f"wrong:{e}")                           