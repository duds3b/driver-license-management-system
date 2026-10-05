-- Create the database
CREATE DATABASE mydb;

USE mydb;

-- People table
CREATE TABLE pessoa (
    Id_pessoa INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100),        -- First name
    Sobrenome VARCHAR(100)    -- Last name
);

-- Driver's licenses table, each license belongs to one person
CREATE TABLE habilitacao (
    Num_Habilitacao VARCHAR(50) PRIMARY KEY,  -- License number
    Validade DATE,                            -- Expiration date
    Pessoa_Id_pessoa INT,                     -- Owner of the license
    FOREIGN KEY (Pessoa_Id_pessoa)
        REFERENCES pessoa(Id_pessoa)
);
