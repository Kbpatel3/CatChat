import React from "react";

const Dashboard = () => {
  // Dashboard logic here

  return (
    <div>
      <section className="bg-gray-50 dark:bg-gray-900">
        <div className="grid grid-cols-5 grid-rows-8 gap-2">
            <div className="row-span-2">

            </div>
            <div className="row-span-6 col-start-1 row-start-3">2</div>
            <div className="col-span-4 col-start-2 row-start-1">3</div>
            <div className="col-span-4 row-span-5 col-start-2 row-start-2">4</div>
            <div className="col-span-4 row-span-2 col-start-2 row-start-7">5</div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
