import React from "react";

import "./Item.css";

const Item = (props) => (
  <div className="item-wrapper flex-wrapper">
    <div style={{ flex: 7 }}>
      <h3 width={100}>
        <a href={`/bucket/${props.item.id}/tasks`}>{props.item.name}</a>
      </h3>
    </div>

    <div style={{ flex: 1 }}>
      <button
        onClick={() => props.self.startEdit(props.item)}
        className="btn btn-sm btn-outline-info"
      >
        Edit
      </button>
    </div>

    <div style={{ flex: 1 }}>
      <button
        onClick={() => props.self.deleteItem(props.item)}
        className="btn btn-sm btn-outline-danger delete"
      >
        Delete
      </button>
    </div>
  </div>
);

export default Item;
