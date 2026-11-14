from app.ingestion import read_transactions 

def test_read_transactions(tmp_path):
    csv_file = tmp_path / "transactions.csv"


    csv_file.write_text(
        "transaction_id,customer_id,amount\n"
        "101,1,250\n"
        "102,,100\n"
    )

    result = read_transactions(csv_file)

    assert len(result) == 2
    assert result[0]["transaction_id"] == 101
    assert result[0]["customer_id"] == 1
    assert result[0]["amount"] == 250 
    assert result[1]["customer_id"] is None 

def test_invalid_csv_values(tmp_path): 
    csv_file = tmp_path / "transactions.csv" 

    csv_file.write_text(
        "transaction_id,customer_id,amount\n"
        "101,1,250\n"
        "abc,2,100\n"
        "103,xyz,200\n"
        "104,4,hello\n"
        "105,5,125.75\n"
    )

    result = read_transactions(csv_file)

    assert len(result) == 5
    assert result[1]["transaction_id"] is None 
    assert result[2]["customer_id"] is None 
    assert result[3]["amount"] is None 
    assert result[4]["amount"] == 125.75


