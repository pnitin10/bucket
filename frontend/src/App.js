import React from "react";
import axios from "axios";

import Item from "./components/Item/Item";
import CustomNavbar from "./components/UI/Navbar/Navbar";

import "./App.css";

class App extends React.Component {
  // Initial App state
  state = {
    itemList: [],
    activeItem: {
      id: null,
      name: "",
    },
    editing: false,
  };

  // Creating csrf token
  getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  componentWillMount() {
    this.fetchItems();
  }

  // Fetching items from database
  fetchItems = () => {
    console.log("Fetching...");
    axios.get("http://127.0.0.1:8000/api/bucket-list/").then((res) => {
      this.setState({ itemList: res.data });
    });
  };

  // On input change
  handleChange = (e) => {
    this.setState({
      activeItem: {
        ...this.state.activeItem,
        [e.target.id]: e.target.value,
      },
    });
  };

  // After submit button
  handleSubmit = (e) => {
    e.preventDefault();
    console.log("ITEM:", this.state.activeItem);

    let form_data = new FormData();
    const csrftoken = this.getCookie("csrftoken");
    let url = "http://127.0.0.1:8000/api/bucket-create/";

    form_data.append("name", this.state.activeItem.name);

    // Updating an item
    if (this.state.editing) {
      url = `http://127.0.0.1:8000/api/bucket-update/${this.state.activeItem.id}/`;
      this.setState({
        editing: false,
      });
    }

    // Creating an item
    axios
      .post(url, form_data, {
        headers: {
          "content-type": `multipart/form-data;`,
          "X-CSRFToken": csrftoken,
        },
      })
      .then((res) => {
        this.fetchItems();
        this.setState({
          activeItem: {
            id: null,
            name: "",
          },
        });
      })
      .catch((err) => console.log("ERROR:", err));
  };

  // Edit Item
  startEdit = (item) => {
    this.setState({
      activeItem: {
        id: item.id,
        name: item.name,
      },
      editing: true,
    });
  };

  // Delete Item
  deleteItem = (item) => {
    var csrftoken = this.getCookie("csrftoken");

    fetch(`http://127.0.0.1:8000/api/bucket-delete/${item.id}/`, {
      method: "DELETE",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    }).then((response) => {
      this.fetchItems();
    });
  };

  render() {
    var items = this.state.itemList;
    var self = this;

    return (
      <>
        <CustomNavbar />
        <div className="container">
          <div id="item-container">
            <center>
              <h2>Add/Edit Bucket</h2>
            </center>
            <div id="form-wrapper">
              <form onSubmit={this.handleSubmit} id="form">
                <div className="flex-wrapper">
                  <div style={{ flex: 6 }}>
                    <input
                      onChange={this.handleChange}
                      className="form-control"
                      id="name"
                      value={this.state.activeItem.name}
                      type="text"
                      name="name"
                      required
                      placeholder="Add bucket.."
                    />
                  </div>
                </div>
                <br />
                <div className="flex-wrapper">
                  <div style={{ flex: 1 }}>
                    <center>
                      <input
                        id="submit"
                        className="btn btn-warning"
                        type="submit"
                        name="Add"
                      />
                    </center>
                  </div>
                </div>
              </form>
            </div>

            <div id="list-wrapper">
              <center>
                <h2>Buckets</h2>
              </center>
              {items.map(function (item, index) {
                return <Item key={item.id} item={item} self={self} />;
              })}
            </div>
          </div>
          <center>
            <h5>XYZ ©2021 Created by Nitin Pahuja</h5>
          </center>
        </div>
      </>
    );
  }
}

export default App;
