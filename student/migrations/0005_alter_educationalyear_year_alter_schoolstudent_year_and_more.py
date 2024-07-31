# Generated by Django 5.0.6 on 2024-07-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_exammarkassingdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalyear',
            name='year',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='schoolstudent',
            name='year',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='students',
            name='admission_date',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='studentsstdmultilist',
            name='year',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='studentsupdatelist',
            name='admission_date',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='studentsupdateshistory',
            name='year',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
        migrations.AlterField(
            model_name='updatestudent',
            name='year',
            field=models.CharField(choices=[('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000')], max_length=50),
        ),
    ]
