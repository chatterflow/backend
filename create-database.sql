CREATE TABLE users (
	id VARCHAR(255) PRIMARY KEY,
	nome_completo VARCHAR(255),
	genero VARCHAR(255) NOT NULL,
	cpf VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	data_nascimento DATE NOT NULL,
	senha VARCHAR(255) NOT NULL,
	preferencia_comunicacao VARCHAR(255) NOT NULL,
	cep VARCHAR(255) NOT NULL,
	telefone VARCHAR(255) NOT NULL,
	endereco VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL
);

CREATE TABLE thread (
	id VARCHAR(255) PRIMARY KEY,
	participant_1 VARCHAR(255) NOT NULL,
	participant_2 VARCHAR(255) NOT NULL
);

CREATE TABLE message (
	id VARCHAR(255) PRIMARY KEY,
	content VARCHAR(255) NOT NULL,
	thread_id VARCHAR(255) NOT NULL,
	sender_id VARCHAR(255) NOT NULL,
	receiver_id VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL
);

CREATE TABLE notifications (
    id VARCHAR(255) PRIMARY KEY,
	message_id VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);


ALTER TABLE thread
	ADD FOREIGN KEY (participant_1) REFERENCES users (id);

ALTER TABLE thread
	ADD FOREIGN KEY (participant_2) REFERENCES users (id);

ALTER TABLE message
	ADD FOREIGN KEY (thread_id) REFERENCES thread (id);

ALTER TABLE message 
	ADD FOREIGN KEY (sender_id) REFERENCES users (id);

ALTER TABLE message 
	ADD FOREIGN KEY (receiver_id) REFERENCES users (id);

ALTER TABLE notifications 
	ADD FOREIGN KEY (message_id) REFERENCES message (id);

