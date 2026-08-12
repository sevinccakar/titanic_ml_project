--select top 10 Age,Fare from dbo.train
--drop table dbo.train
 
--CREATE TABLE dbo.train 
--( PassengerId INT, Survived INT, Pclass INT, Name NVARCHAR(200),
--Sex VARCHAR(10), Age FLOAT NULL, SibSp INT, Parch INT, 
--Ticket VARCHAR(50), Fare FLOAT, Cabin VARCHAR(20) NULL,
--Embarked VARCHAR(5) NULL );

--BULK INSERT dbo.train 
--FROM 'C:\Users\sevin\Desktop\Python\train.csv'
--WITH ( FIRSTROW = 2, FORMAT = 'CSV', FIELDQUOTE = '"', 
--FIELDTERMINATOR = ',', ROWTERMINATOR = '0x0a',
--CODEPAGE = '65001', TABLOCK );

--select top 10 Age, Fare from dbo.train

UPDATE dbo.train
SET Embarked = REPLACE(Embarked, CHAR(13), '')
WHERE Embarked LIKE '%' + CHAR(13);