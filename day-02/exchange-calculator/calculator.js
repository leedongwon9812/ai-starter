'use strict';
function parseRates(csv) {
  const rows = csv.replace(/^\uFEFF/, '').trim().split(/\r?\n/).map(line => line.split(',').map(x => x.trim().replace(/^"(.*)"$/, '$1')));
  if (rows[0].join(',') !== 'date,base,currency,rate') throw new Error('CSV 열은 date,base,currency,rate 순서여야 합니다.');
  const rates = { USD: 1 };
  let date;
  for (const row of rows.slice(1)) {
    const [d, base, currency, value] = row;
    if (row.length !== 4 || !/^\d{4}-\d{2}-\d{2}$/.test(d) || base !== 'USD' || !['KRW','JPY','EUR'].includes(currency) || currency in rates || !Number.isFinite(Number(value)) || Number(value) <= 0 || (date && date !== d)) throw new Error('CSV의 날짜, 통화 또는 환율을 확인해 주세요.');
    date = d; rates[currency] = Number(value);
  }
  if (Object.keys(rates).length !== 4) throw new Error('KRW, JPY, EUR 환율이 모두 필요합니다.');
  return { date, rates };
}
function convert(amount, from, to, rates) {
  if (!Number.isFinite(amount) || amount < 0) throw new Error('0 이상의 금액을 입력해 주세요.');
  const result = amount * (rates[to] / rates[from]);
  if (!Number.isFinite(result)) throw new Error('금액이 너무 큽니다.');
  return result;
}
if (typeof module !== 'undefined') module.exports = { parseRates, convert };
if (typeof document !== 'undefined') {
  const $ = id => document.getElementById(id);
  let data;
  const fmt = (n, digits = 2) => new Intl.NumberFormat('ko-KR', { maximumFractionDigits: digits }).format(n);
  function calculate() {
    if (!data) return;
    try {
      if (!$('amount').value.trim()) throw new Error('금액을 입력해 주세요.');
      const from = $('from').value, to = $('to').value;
      $('result').textContent = `${fmt(convert(Number($('amount').value), from, to, data.rates))} ${to}`;
      $('equation').textContent = `1 ${from} = ${fmt(data.rates[to] / data.rates[from], 6)} ${to}`;
      $('error').textContent = '';
    } catch (e) { $('result').textContent = '—'; $('error').textContent = e.message; }
  }
  function load(csv, label) {
    data = parseRates(csv);
    $('status').textContent = `기준일 ${data.date} · ${label}`;
    $('cards').replaceChildren(...['KRW','JPY','EUR'].map(currency => {
      const div = document.createElement('div');
      const title = document.createElement('span'); title.textContent = currency;
      const value = document.createElement('strong'); value.textContent = fmt(data.rates[currency], 5);
      div.append(title, value); return div;
    }));
    calculate();
  }
  for (const id of ['amount','from','to']) $(id).addEventListener('input', calculate);
  $('swap').onclick = () => { const prev = $('from').value; $('from').value = $('to').value; $('to').value = prev; calculate(); };
  $('file').onchange = async event => {
    const file = event.target.files[0]; if (!file) return;
    try { load(await file.text(), file.name); }
    catch (e) { data = undefined; $('result').textContent = '—'; $('equation').textContent = ''; $('cards').replaceChildren(); $('status').textContent = 'CSV를 다시 선택해 주세요.'; $('error').textContent = e.message; }
  };
  (async () => {
    try {
      if (location.protocol === 'file:') load(window.savedCsv, '저장된 CSV 사본');
      else { const response = await fetch('./exchange-rates.csv', { cache: 'no-store' }); if (!response.ok) throw new Error('CSV를 불러오지 못했습니다.'); load(await response.text(), 'exchange-rates.csv'); }
    } catch (e) { $('error').textContent = 'CSV 파일을 선택해 환율을 불러와 주세요.'; }
  })();
}
