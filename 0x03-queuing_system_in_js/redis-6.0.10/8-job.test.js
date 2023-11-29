// Test for Job creation
import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function () {
  const Spy = sinon.spy(console);
  const queue = createQueue({ name: 'push_notification_code_test' });

  before(function () {
    queue.testMode.enter(true);
  });

  after(function () {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  afterEach(function () {
    Spy.log.resetHistory();
  });

  it('error message displayed if jobs is not an array', function () {
    expect(
      createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, queue)
    ).to.throw('Jobs is not an array');
  });

  it('adds created jobs to the queue with the correct type', function (done) {
    expect(queue.testMode.jobs.length).to.equal(0);
    const jobInfos = [
      {
        phoneNumber: '4153518780',
        message: 'The code 1234 to verify your account',
      },
      {
        phoneNumber: '5153518781',
        message: 'The code 1738 to verify your account',
      },
    ];
    createPushNotificationsJobs(jobInfos, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobInfos[0]);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    queue.process('push_notification_code_3', function () {
      expect(
        Spy.log
          .calledWithMatch('Notification job created:', queue.testMode.jobs[0].id)
      ).to.be.true;
      done();
    });
  });

  it('registers the progress event handler for a job', function (done) {
    queue.testMode.jobs[0].addListener('progress', function () {
      expect(
        Spy.log
          .calledWithMatch('Notification job', queue.testMode.jobs[0].id, '25% complete')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('progress', 25);
  });

  it('registers the failed event handler for a job', function (done) {
    queue.testMode.jobs[0].addListener('failed', function () {
      expect(
        Spy.log
          .calledWithMatch('Notification job', queue.testMode.jobs[0].id, 'failed:')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('registers the complete event handler for a job', function (done) {
    queue.testMode.jobs[0].addListener('complete', function () {
      expect(
        Spy.log
          .calledWithMatch('Notification job', queue.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('complete');
  });
});
