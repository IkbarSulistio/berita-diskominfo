import streamlit as st
import pandas as pd

st.set_page_config(page_title="Penilaian Berita Diskominfo", layout="wide")
st.title("📊 Penilaian Berita Diskominfo Kaltim")

uploaded_file = st.file_uploader("📁 Unggah file Excel laporan berita (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    df.columns = ['NO', 'TANGGAL', 'JUDUL BERITA', 'PETUGAS PELIPUT', 'FOTO/SUMBER', 'BIDANG', 'JENIS BERITA', 'VIEWERS']
    df = df[df['TANGGAL'].notna()]
    df.reset_index(drop=True, inplace=True)

    def nilai_berita(row):
        try:
            viewers = int(row['VIEWERS'])
        except:
            viewers = 0

        skor_viewers = 3 if viewers > 5000 else 2 if viewers >= 1000 else 1

        bidang = str(row['BIDANG']).lower()
        skor_bidang = 3 if any(x in bidang for x in ['ekonomi', 'pemerintahan', 'keamanan']) \
                     else 2 if any(x in bidang for x in ['berita', 'pengumuman', 'hiburan']) else 1

        sumber = str(row['FOTO/SUMBER']).lower()
        skor_sumber = 3 if any(x in sumber for x in ['kemkom', 'bawaslu', 'resmi']) \
                      else 2 if sumber and sumber != 'nan' else 1

        total_skor = skor_viewers + skor_bidang + skor_sumber
        kategori = 'Penting' if total_skor >= 8 else 'Umum' if total_skor >= 5 else 'Rendah Prioritas'

        return pd.Series([skor_viewers, skor_bidang, skor_sumber, total_skor, kategori],
                         index=['Skor Viewers', 'Skor Bidang', 'Skor Sumber', 'Total Skor', 'Kategori'])

    df[['Skor Viewers', 'Skor Bidang', 'Skor Sumber', 'Total Skor', 'Kategori']] = df.apply(nilai_berita, axis=1)

    st.success("✅ Berita berhasil dinilai.")
    st.dataframe(df[['TANGGAL', 'JUDUL BERITA', 'PETUGAS PELIPUT', 'VIEWERS', 'BIDANG', 'FOTO/SUMBER', 'Kategori']])

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh CSV", csv, "hasil_penilaian_berita.csv", "text/csv")

else:
    st.info("Silakan unggah file Excel terlebih dahulu.")

