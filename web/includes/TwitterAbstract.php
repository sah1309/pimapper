<?php
/**
 * web -- bootstrap.php
 * User: Simon Beattie
 * Date: 18/12/2013
 * Time: 16:51
 */

class StatusAbstract
{

    /**
     * @var PDO $pdo
     */
    protected $pdo;

    /**
     * @var array $config
     */
    protected $config;

    /**
     * @var array $oauth
     */
    protected $oauth;

    public function __construct(PDO $pdo, array $config, $oauth)
    {
        $this->setPdo($pdo);
        $this->setConfig($config);
        $this->setOauth($oauth);
    }

    /**
     * setConfig sets the config property in object storage
     *
     * @param array $config
     * @throws InvalidArgumentException
     * @return StatusAbstract
     */
    public function setConfig($config)
    {
        if (empty($config)) {
            throw new \InvalidArgumentException(__METHOD__ . ' cannot accept an empty config');
        }
        $this->config = $config;
        return $this;
    }

    /**
     * getConfig returns the config from the object
     *
     * @return array
     */
    public function getConfig()
    {
        return $this->config;
    }

    /**
     * setPdo sets the pdo property in object storage
     *
     * @param \PDO $pdo
     * @throws InvalidArgumentException
     * @return StatusAbstract
     */
    public function setPdo($pdo)
    {
        if (empty($pdo)) {
            throw new \InvalidArgumentException(__METHOD__ . ' cannot accept an empty pdo');
        }
        $this->pdo = $pdo;
        return $this;
    }

    /**
     * getPdo returns the pdo from the object
     *
     * @return \PDO
     */
    public function getPdo()
    {
        return $this->pdo;
    }


    public function setOauth($oauth)
    {
        if (empty($oauth)) {
            throw new \InvalidArgumentException(__METHOD__ . ' cannot accept an empty Oauth object');
        }
        $this->oauth = $oauth;
        return $this;
    }

    public function getOauth()
    {
        return $this->oauth;
    }
}