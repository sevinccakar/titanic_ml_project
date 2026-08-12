CREATE TABLE dbo.train (
    PassengerId INT PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name NVARCHAR(200),
    Sex VARCHAR(10),
    Age FLOAT NULL,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(20) NULL,
    Embarked VARCHAR(5) NULL
);

BULK INSERT dbo.train
FROM 'C:\Users\sevin\Desktop\Python\train.csv'
WITH (
    FIRSTROW = 2,
    FORMAT = 'CSV',
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK
);

UPDATE dbo.train
SET Embarked = REPLACE(Embarked, CHAR(13), '')
WHERE Embarked LIKE '%' + CHAR(13);

SELECT TOP 10 *
FROM dbo.train;
