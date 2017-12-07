Title: Redux 架構下實作 Async Actions
Slug: redux-async-action
Date: 2016-04-26 14:37:54
Categories: Reactjs
Tags: reactjs,redux,async,action
---
最近專案開發上使用了 reactjs ，並採用`redux`架構。而依照 javascript 的特性，你沒辦法假設他會將指令執行完才繼續下一道指令，所以要怎麼做到多個 Action 異步處理呢？

舉個例子，當你 update 一份資料以後，希望他能隨後就 fetch 回來，以確保 state 裡面都是最新的資料，直觀的來寫會是這樣，但眼尖的你一定會發現不太對勁。
```js
export const fetchData = createAction('FETCH_DATA', APIUtil.fetchData);
export const updateData = createAction('UPDATE_DATA', APIUtil.updateData);
```
```js
this.props.updateData(data);
this.props.fetchData(); // not latest result
```
它不會等 `updateData` 執行完才執行 `fetchData`，這樣會有順序性上的錯誤。所以我們可以在 Action 裡面動手腳，以確保`fetch`會在`update`之後。
```js
export const fetchData = createAction('FETCH_DATA', APIUtil.fetchData);
export function updateEventData(id, data) {
  return (dispatch) => (
    APIUtil.updateData(data)
      .then(() => dispatch(fetchData()));
  );
}
```
不要用內建的`createAction`，改成自己定義 Action 就能解決這個問題囉！

## Go Deeper
[http://redux.js.org/docs/advanced/AsyncActions.html](http://redux.js.org/docs/advanced/AsyncActions.html)
