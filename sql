CREATE TABLE qrcode (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    status varchar(255),
    qrcode varchar(255),
    img_link varchar(255),
    create_date timestamp NOT NULL DEFAULT current_timestamp(),
    update_date timestamp ON UPDATE current_timestamp(),
    PRIMARY KEY (id)
) ENGINE = InnoDB;

CREATE TABLE qrlogs (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    create_date timestamp NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY (id),
    CONSTRAINT `fk_qrcode_qrlogs`
      FOREIGN KEY (qrcode_id) REFERENCES qrcode(id)
      ON DELETE CASCADE
      ON UPDATE RESTRICT

) ENGINE = InnoDB;