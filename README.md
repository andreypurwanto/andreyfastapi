# andreyfastapi

## Heroku
https://andreyfastapi.herokuapp.com/ </br>
https://andreyfastapi.herokuapp.com/docs/ </br>

## Endpoint
1. / : return active endpoint </br>
- return example </br>
`{
  "1": "/selisih/",
  "2": "/pilihdata/"
}`
</br>

2. /pilihdata/ : return slice data input </br>
- parameters : </br>
    - initialdate (str) : "yyyymmdd" default 20200401
    - enddate (str) : "yyyymmdd" default 20200401
    - kecamatan_ : 'all' for all list, or sliced by comma </br>
list of kecamatan : </br>
`['CAKUNG' 'CEMPAKA PUTIH' 'CENGKARENG' 'CILANDAK' 'CILINCING' 'CIPAYUNG'
 'CIRACAS' 'DUREN SAWIT' 'GAMBIR' 'GROGOL PETAMBURAN' 'JAGAKARSA'
 'JATINEGARA' 'JOHAR BARU' 'KALI DERES' 'KEBAYORAN BARU' 'KEBAYORAN LAMA'
 'KEBON JERUK' 'KELAPA GADING' 'KEMAYORAN' 'KEMBANGAN'
 'KEP. SERIBU SELATAN' 'KEP. SERIBU UTARA' 'KOJA' 'KRAMAT JATI'
 'LUAR DKI JAKARTA' 'MAKASAR' 'MAMPANG PRAPATAN' 'MATRAMAN' 'MENTENG'
 'PADEMANGAN' 'PALMERAH' 'PANCORAN' 'PASAR MINGGU' 'PASAR REBO'
 'PENJARINGAN' 'PESANGGRAHAN' 'PULO GADUNG' 'SAWAH BESAR' 'SENEN'
 'SETIA BUDI' 'TAMAN SARI' 'TAMBORA' 'TANAH ABANG' 'TANJUNG PRIOK' 'TEBET']` </br>
 ex : CAKUNG,TEBET,PESANGGRAHAN
- return column same as data input, but only sliced between parameters
- return example </br>
    - https://andreyfastapi.herokuapp.com/pilihdata/?initialdate=20200330&enddate=20200330&kecamatan_=CAKUNG%2CTEBET%2CPESANGGRAHAN </br>
    - `{
  "query": {
    "kecamatan": "CAKUNG,TEBET,PESANGGRAHAN",
    "initialdate": "2020-03-30 00:00:00",
    "enddate": "2020-03-30 00:00:00"
  },
  "data ": {
    "0": {
      "tanggal": "2020-03-30T00:00:00",
      "kecamatan": "CAKUNG",
      "odp": 18,
      "proses_pemantauan": 5,
      "selesai_pemantauan": 13,
      "pdp": 21,
      "masih_dirawat": 14,
      "pulang_dan_sehat": 7,
      "positif": 10,
      "dirawat": 7,
      "sembuh": 0,
      "meninggal": 2,
      "isolasi_mandiri": 1
    },
    "1": {
      "tanggal": "2020-03-30T00:00:00",
      "kecamatan": "PESANGGRAHAN",
      "odp": 19,
      "proses_pemantauan": 0,
      "selesai_pemantauan": 19,
      "pdp": 18,
      "masih_dirawat": 15,
      "pulang_dan_sehat": 3,
      "positif": 19,
      "dirawat": 5,
      "sembuh": 0,
      "meninggal": 6,
      "isolasi_mandiri": 8
    },
    "2": {
      "tanggal": "2020-03-30T00:00:00",
      "kecamatan": "TEBET",
      "odp": 18,
      "proses_pemantauan": 1,
      "selesai_pemantauan": 17,
      "pdp": 18,
      "masih_dirawat": 11,
      "pulang_dan_sehat": 7,
      "positif": 14,
      "dirawat": 11,
      "sembuh": 0,
      "meninggal": 3,
      "isolasi_mandiri": 0
    }
  }
}`
</br>
</br>

3. /selisih/ : return analysis of difference and rate of positif case, difference and rate of 'sembuh' case and difference and rate of 'meninggal' case  with differences between initial and end date sliced by parameters of : initialdate, enddate, kecamatan_, sort_by, ascending_, top_rank </br>

- parameters : </br>
    - initialdate (str) : "yyyymmdd" default 20200325
    - enddate (str) : "yyyymmdd" default 20200603
    - kecamatan_ (str): 'all' for all list, or sliced by comma, same as above, default all </br>
    - sort_by : sort by parameters, default 0 </br>
    '0' sort by kecamatan </br>
    '1' sort by positif_selisih_nilai </br>
    '2' sort by positif_selisih_persentase </br>
    '3 sort by sembuh_selisih_nilai </br>
    '4' sort by sembuh_selisih_persentase </br>
    '5' sort by meninggal_selisih_nilai </br>
    '6' sort by meninggal_selisih_persentase </br>
    - ascending_ : 1 True, 0 False, default 1
    - top_rank : sliced by rank, default 10 </br>
    example:</br>
    '5' return top 5 </br>
    '2-8' return rank 2 till rank 8 </br>
- return  </br>
{ "query": </br> { 
    "tanggal_awal": "query initial date", </br> "tanggal_akhir": "query initial date", </br>
    "kecamatan": "all", </br> 
    "sort_by": ""query sort" by", </br> 
    "ascending_": "query ascending", </br> 
    "top_rank": "3" },  </br>
    "data":  </br>
    { "0": { "kecamatan": "kecamatan x",  "positif_selisih_nilai": "difference positif value between end date and initial date ", </br>
    "positif_selisih_persentase": rate positif value between end date and initial date,</br>
     "sembuh_selisih_nilai": difference 'sembuh' value between end date and initial date, </br>
     "sembuh_selisih_persentase": rate 'sembuh' value between end date and initial date, </br>
     "meninggal_selisih_nilai": difference 'meninggal' value between end date and initial date, </br>
     "meninggal_selisih_persentase": rate 'meninggal' value between end date and initial date } </br>
     '1': {...} </br>
     ... </br>
     }</br>

- return example
    - https://andreyfastapi.herokuapp.com/selisih/?initialdate=20200401&enddate=20200501&kecamatan_=all&sort_by=1&ascending_=0&top_rank=3
    - `{
  "query": {
    "tanggal_awal": "2020-04-01 00:00:00",
    "tanggal_akhir": "2020-05-01 00:00:00",
    "kecamatan": "all",
    "sort_by": "positif_selisih_nilai",
    "ascending_": 0,
    "top_rank": "3"
  },
  "data": {
    "0": {
      "kecamatan": "LUAR DKI JAKARTA",
      "positif_selisih_nilai": 670,
      "positif_selisih_persentase": 632.0754716981132,
      "sembuh_selisih_nilai": 60,
      "sembuh_selisih_persentase": 1200,
      "meninggal_selisih_nilai": 44,
      "meninggal_selisih_persentase": 440.00000000000006
    },
    "1": {
      "kecamatan": "TANAH ABANG",
      "positif_selisih_nilai": 208,
      "positif_selisih_persentase": 4160,
      "sembuh_selisih_nilai": 4,
      "sembuh_selisih_persentase": 200,
      "meninggal_selisih_nilai": 11,
      "meninggal_selisih_persentase": "undefined"
    },
    "2": {
      "kecamatan": "TANJUNG PRIOK",
      "positif_selisih_nilai": 131,
      "positif_selisih_persentase": 1007.6923076923076,
      "sembuh_selisih_nilai": 7,
      "sembuh_selisih_persentase": 700,
      "meninggal_selisih_nilai": 14,
      "meninggal_selisih_persentase": 1400
    }
  }
}`

## Data Used
https://data.go.id/dataset/data-odp-pdp-dan-positif-covid-19-dki-jakarta-per-kecamatan </br>
