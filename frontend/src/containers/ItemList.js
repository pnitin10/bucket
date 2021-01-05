import React, { Component } from "react";
import axios from "axios";

import Item from "../components/Item/Item";

class ItemList extends Component {
  state = {
    itemList: [],
  };

  componentWillMount() {
    console.log();
    this.fetchItems();
  }

  fetchItems = () => {
    console.log("Fetching...");
    axios.get("http://127.0.0.1:8000/api/item-list/").then((res) => {
      this.setState({ itemList: res.data });
    });
  };

  render() {
    var items = this.state.itemList;
    var self = this;

    return items.map(function (item, index) {
      return <Item item={item} index={index} self={self} key={item.id} />;
    });
  }
}

export default ItemList;
