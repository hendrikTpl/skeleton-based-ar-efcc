## Database format
- Every request will be saved in global_database by format unique_id, ip_addr, date, and the json_path
- Action_database is responsible to save the predicted action by format ip_addr, unique_id used for prediction, and the label.

## Prequesities
- [ ] Install MongoDB (Todo)
- [ ] Make Database Helper (Todo)
- [ ] Save data every request received in server.
- [ ] Autmatic Sliding Window by total received data
- [ ] Data transform: 
    - 16 Points --> 15 Points - same with UT
    - Transform to GCN Format
- [ ] JSON -> NPY; using data generator from ST-GCN DATAGEN 
- [ ] Action Prediction using ST-GCN-PAM
