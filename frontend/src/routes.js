import React from "react";
import { Route } from "react-router-dom";

import App from "./App";
import BucketTasks from "./containers/BucketTasks";

const BaseRouter = () => (
  <div>
    <Route exact path="/" component={App} />
    <Route exact path="/bucket/:bucketID/tasks" component={BucketTasks} />
  </div>
);

export default BaseRouter;
