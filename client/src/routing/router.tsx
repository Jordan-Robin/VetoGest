import { createBrowserRouter } from "react-router-dom";
import { PATHS } from "./routingPaths";
import { App } from "@/App";
import { LoginForm } from "@/features/auth/components/LoginForm/LoginForm";
import { CreateCustomerForm } from "@/features/customers/components/CreateCustomerForm";

export const router = createBrowserRouter([
  {
    path: PATHS.HOME,
    element: <App />,
    children: [
      {
        index: true,
        element: <CreateCustomerForm />,
      },
      {
        path: PATHS.LOGIN,
        element: <LoginForm />,
      },
    ],
  },
]);
