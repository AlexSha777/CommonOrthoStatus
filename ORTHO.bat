pyinstaller --onedir --noconsole ^
--add-data="back_clear.bmp;." ^
--add-data="body.bmp;." ^
--add-data="foot_movements.bmp;." ^
--add-data="front_clear.bmp;." ^
--add-data="Ped_d.bmp;." ^
--add-data="Ped_s.bmp;." ^
--add-data="sagit_vertebra_fit.bmp;." ^
--add-data="vertebra.bmp;." ^
--add-data="wrists_l.bmp;." ^
--add-data="wrists_r.bmp;." ^
--add-data="samples_diagnosis.pickle;." ^
--add-data="samples_manipulation.pickle;." ^
--add-data="samples_appointment.pickle;." ^
--add-data="samples_recomendation.pickle;." ^
--add-data="icon.ico;." ^
--icon=icon.ico ^
--clean ^
ORTHO_STATUS.py