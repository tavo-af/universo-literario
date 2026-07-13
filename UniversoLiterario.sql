
-- Base de Datos: UniversoLiterario
CREATE DATABASE IF NOT EXISTS UniversoLiterario;
USE UniversoLiterario;

CREATE TABLE Autores(
 id_autor INT PRIMARY KEY,
 nombre VARCHAR(50),
 apellido VARCHAR(50),
 nacionalidad VARCHAR(50)
);

CREATE TABLE Editoriales(
 id_editorial INT PRIMARY KEY,
 nombre VARCHAR(100),
 telefono VARCHAR(20)
);

CREATE TABLE Categorias(
 id_categoria INT PRIMARY KEY,
 nombre VARCHAR(50)
);

CREATE TABLE Usuarios(
 id_usuario INT PRIMARY KEY,
 nombre VARCHAR(50),
 apellido VARCHAR(50),
 telefono VARCHAR(20)
);

CREATE TABLE Empleados(
 id_empleado INT PRIMARY KEY,
 nombre VARCHAR(50),
 cargo VARCHAR(50)
);

CREATE TABLE Libros(
 id_libro INT PRIMARY KEY,
 titulo VARCHAR(100),
 id_autor INT,
 id_editorial INT,
 id_categoria INT,
 existencias INT,
 FOREIGN KEY(id_autor) REFERENCES Autores(id_autor),
 FOREIGN KEY(id_editorial) REFERENCES Editoriales(id_editorial),
 FOREIGN KEY(id_categoria) REFERENCES Categorias(id_categoria)
);

CREATE TABLE Prestamos(
 id_prestamo INT PRIMARY KEY,
 id_usuario INT,
 id_empleado INT,
 fecha_prestamo DATE,
 FOREIGN KEY(id_usuario) REFERENCES Usuarios(id_usuario),
 FOREIGN KEY(id_empleado) REFERENCES Empleados(id_empleado)
);

CREATE TABLE Devoluciones(
 id_devolucion INT PRIMARY KEY,
 id_prestamo INT,
 fecha_devolucion DATE,
 FOREIGN KEY(id_prestamo) REFERENCES Prestamos(id_prestamo)
);

CREATE TABLE Multas(
 id_multa INT PRIMARY KEY,
 id_usuario INT,
 monto DECIMAL(8,2),
 motivo VARCHAR(100),
 FOREIGN KEY(id_usuario) REFERENCES Usuarios(id_usuario)
);

INSERT INTO Autores VALUES
(1,'Gabriel','Garcia Marquez','Colombia'),
(2,'Julio','Cortazar','Argentina'),
(3,'Mario','Vargas Llosa','Peru'),
(4,'Jorge Luis','Borges','Argentina'),
(5,'Isabel','Allende','Chile'),
(6,'Octavio','Paz','Mexico'),
(7,'Carlos','Fuentes','Mexico'),
(8,'Laura','Esquivel','Mexico'),
(9,'Juan','Rulfo','Mexico'),
(10,'Pablo','Neruda','Chile');

INSERT INTO Editoriales VALUES
(1,'Planeta','5550001'),
(2,'Penguin','5550002'),
(3,'Alfaguara','5550003'),
(4,'Anagrama','5550004'),
(5,'Santillana','5550005'),
(6,'Debolsillo','5550006'),
(7,'Seix Barral','5550007'),
(8,'Paidos','5550008'),
(9,'Porrua','5550009'),
(10,'Océano','5550010');

INSERT INTO Categorias VALUES
(1,'Novela'),
(2,'Ciencia Ficcion'),
(3,'Fantasia'),
(4,'Poesia'),
(5,'Drama'),
(6,'Historia'),
(7,'Terror'),
(8,'Romance'),
(9,'Aventura'),
(10,'Ensayo');

INSERT INTO Usuarios VALUES
(1,'Ana','Lopez','5511111111'),
(2,'Luis','Perez','5511111112'),
(3,'Maria','Diaz','5511111113'),
(4,'Jose','Ruiz','5511111114'),
(5,'Elena','Torres','5511111115'),
(6,'Carlos','Mora','5511111116'),
(7,'Diana','Rios','5511111117'),
(8,'Jorge','Luna','5511111118'),
(9,'Patricia','Soto','5511111119'),
(10,'Ricardo','Vega','5511111120');

INSERT INTO Empleados VALUES
(1,'Pedro','Bibliotecario'),
(2,'Lucia','Bibliotecaria'),
(3,'Raul','Supervisor'),
(4,'Marta','Auxiliar'),
(5,'Ivan','Auxiliar'),
(6,'Noemi','Recepcionista'),
(7,'Oscar','Catalogador'),
(8,'Julia','Archivista'),
(9,'Sergio','Auxiliar'),
(10,'Monica','Bibliotecaria');

INSERT INTO Libros VALUES
(1,'Libro 1',1,1,1,5),
(2,'Libro 2',2,2,2,6),
(3,'Libro 3',3,3,3,7),
(4,'Libro 4',4,4,4,8),
(5,'Libro 5',5,5,5,4),
(6,'Libro 6',6,6,6,5),
(7,'Libro 7',7,7,7,3),
(8,'Libro 8',8,8,8,9),
(9,'Libro 9',9,9,9,5),
(10,'Libro 10',10,10,10,6);

INSERT INTO Prestamos VALUES
(1,1,1,'2026-01-01'),
(2,2,2,'2026-01-02'),
(3,3,3,'2026-01-03'),
(4,4,4,'2026-01-04'),
(5,5,5,'2026-01-05'),
(6,6,6,'2026-01-06'),
(7,7,7,'2026-01-07'),
(8,8,8,'2026-01-08'),
(9,9,9,'2026-01-09'),
(10,10,10,'2026-01-10');

INSERT INTO Devoluciones VALUES
(1,1,'2026-01-08'),
(2,2,'2026-01-09'),
(3,3,'2026-01-10'),
(4,4,'2026-01-11'),
(5,5,'2026-01-12'),
(6,6,'2026-01-13'),
(7,7,'2026-01-14'),
(8,8,'2026-01-15'),
(9,9,'2026-01-16'),
(10,10,'2026-01-17');

INSERT INTO Multas VALUES
(1,1,50,'Retraso'),
(2,2,25,'Retraso'),
(3,3,75,'Daño'),
(4,4,30,'Retraso'),
(5,5,40,'Retraso'),
(6,6,60,'Daño'),
(7,7,20,'Retraso'),
(8,8,35,'Retraso'),
(9,9,80,'Daño'),
(10,10,25,'Retraso');

USE UniversoLiterario;

ALTER TABLE Libros
MODIFY COLUMN id_libro INT AUTO_INCREMENT;

ALTER TABLE Multas
MODIFY COLUMN id_multa INT AUTO_INCREMENT;

ALTER TABLE Prestamos
MODIFY COLUMN id_prestamo INT AUTO_INCREMENT;

ALTER TABLE Autores
MODIFY COLUMN id_autor INT AUTO_INCREMENT;

ALTER TABLE Editoriales
MODIFY COLUMN id_editorial INT AUTO_INCREMENT;

ALTER TABLE Categorias
MODIFY COLUMN id_categoria INT AUTO_INCREMENT;

ALTER TABLE Usuarios
MODIFY COLUMN id_usuario INT AUTO_INCREMENT;

ALTER TABLE Empleados
MODIFY COLUMN id_empleado INT AUTO_INCREMENT;

ALTER TABLE Devoluciones
MODIFY COLUMN id_devolucion INT AUTO_INCREMENT;

SHOW CREATE TABLE Multas;

USE UniversoLiterario;

ALTER TABLE Multas
MODIFY COLUMN id_multa INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Prestamos
MODIFY COLUMN id_prestamo INT NOT NULL AUTO_INCREMENT;

SHOW CREATE TABLE Prestamos;

ALTER TABLE Prestamos
MODIFY COLUMN id_prestamo INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Multas
MODIFY COLUMN id_multa INT NOT NULL AUTO_INCREMENT;



ALTER TABLE Devoluciones
DROP FOREIGN KEY devoluciones_ibfk_1;

ALTER TABLE Prestamos
MODIFY COLUMN id_prestamo INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Devoluciones
ADD CONSTRAINT devoluciones_ibfk_1
FOREIGN KEY (id_prestamo)
REFERENCES Prestamos(id_prestamo);


ALTER TABLE Devoluciones
DROP FOREIGN KEY devoluciones_ibfk_1;


ALTER TABLE Devoluciones
ADD CONSTRAINT devoluciones_ibfk_1
FOREIGN KEY (id_prestamo)
REFERENCES Prestamos(id_prestamo)
ON DELETE CASCADE;