import INotification from "@/lib/interfaces/INotification";
import { Button } from "@nextui-org/react";
import { Drawer } from "flowbite-react";
import { FaBell } from "react-icons/fa6";
import NotificationItem from "../NotificationItem/NotificationItem";

type Props = {
  isOpen: boolean;
  isLoading: boolean;
  handleClose: Function;
  notifications: INotification[];
  isError?: boolean;
};

const NotificationDrawer = (props: Props) => {
  return (
    <Drawer
      open={props.isOpen}
      onClose={() => props.handleClose()}
      position="right"
      className="max-sm:w-full"
    >
      <Drawer.Header title="Alertas" titleIcon={FaBell} />
      <Drawer.Items>
        <div className="flex flex-col items-center gap-4">
          {props.isError && (
            <p className="text-sm pt-4 text-danger">
              Error al cargar las alertas
            </p>
          )}

          {props.notifications?.length === 0 && (
            <p className="text-sm pt-4  ">No hay nuevas alertas</p>
          )}

          {props.notifications?.map((notification: any) => (
            <NotificationItem
              key={notification.id}
              notification={notification}
            />
          ))}
        </div>

        <div className="flex justify-center pt-4">
          <Button size="sm" variant="ghost" color="primary">
            Ver todas
          </Button>
        </div>
      </Drawer.Items>
    </Drawer>
  );
};

export default NotificationDrawer;
